# -*- coding: utf-8 -*-
import copy
import logging
import os
import re
import sys
from datetime import datetime


# Test logs are written next to the pytest-html reports (tests/test_output/logs/) with a timestamp in
# the filename, so they are easy to find after a run.
_libs_dir = os.path.dirname(os.path.abspath(__file__))          # .../ARCA_source-Git/tests/libs
_repo_root = os.path.dirname(os.path.dirname(_libs_dir))        # .../ARCA_source-Git
_log_dir = os.path.join(_repo_root, "tests", "test_output", "logs")
os.makedirs(_log_dir, exist_ok=True)
_log_path = os.path.join(_log_dir, f"test_run_{datetime.now():%Y%m%d_%H%M%S}.log")

# Write a UTF-8 BOM into a fresh log file so editors (e.g. Notepad) auto-detect the encoding and do
# not render Portuguese characters as mojibake ("Ã§Ã£o"). The FileHandler below opens in append mode,
# so it writes right after the BOM. Also required here because app logs are forwarded into this file.
if not os.path.exists(_log_path) or os.path.getsize(_log_path) == 0:
    with open(_log_path, "wb") as _f:
        _f.write(b"\xef\xbb\xbf")

# --------------------------------------------------------------------------------------------------
# Colors (ANSI escape codes)
# --------------------------------------------------------------------------------------------------
# Set LOG_FILE_COLORS=1 to keep the ANSI colors inside the .log file too. Only do that if you read the
# file with something that renders ANSI (``less -R``, ``bat``, VS Code + an ANSI extension, ...).
# By default the codes are stripped from the file so Notepad & co. show clean text instead of "[1m".
_KEEP_COLORS_IN_FILE = os.getenv("LOG_FILE_COLORS", "0") == "1"

# Matches ANSI escape sequences:
#   - CSI, e.g. "\x1b[1m" (bold) or "\x1b[0m" (reset);
#   - OSC, e.g. "\x1b]9;4;1;20\x1b\\" (pytest >= 9 progress bar in Windows Terminal), terminated by
#     BEL ("\x07") or ST ("\x1b\\").
_ANSI_RE = re.compile(
    r"\x1b\[[0-9;?]*[A-Za-z]"
    r"|\x1b\][^\x07\x1b]*(?:\x07|\x1b\\)"
)

# Legacy Windows consoles only interpret ANSI after "virtual terminal processing" is enabled.
# Calling os.system("") is the well-known trick that turns it on (no-op elsewhere).
if os.name == "nt":
    os.system("")


def _stream_supports_color(stream):
    """Decide whether the console should receive colored output."""
    if os.getenv("NO_COLOR"):
        return False
    if os.getenv("FORCE_COLOR") or os.getenv("PY_COLORS") == "1":
        return True
    return hasattr(stream, "isatty") and stream.isatty()


class ColorFormatter(logging.Formatter):
    """Colors only the level name and lets the message pass through untouched.

    Colors are NOT wrapped around the whole line on purpose: messages that already carry ANSI codes
    (e.g. pytest's bold "collecting ...") end with a reset code that would cancel an outer color."""

    _LEVEL_COLORS = {
        logging.DEBUG: "\x1b[36m",       # cyan
        logging.INFO: "\x1b[32m",        # green
        logging.WARNING: "\x1b[33m",     # yellow
        logging.ERROR: "\x1b[31m",       # red
        logging.CRITICAL: "\x1b[1;31m",  # bold red
    }
    _RESET = "\x1b[0m"

    def format(self, record):
        color = self._LEVEL_COLORS.get(record.levelno, "")
        # Work on a copy: the very same record is handed to every handler, and the file handler
        # must not see the colored level name.
        record = copy.copy(record)
        # Pad *before* adding the escape codes so the "-8s" alignment is not thrown off by them.
        record.levelname = f"{color}{record.levelname:<8}{self._RESET}"
        return super().format(record)


class PlainFormatter(logging.Formatter):
    """Removes every ANSI escape sequence from the final line (used where colors are not rendered)."""

    def format(self, record):
        return _ANSI_RE.sub("", super().format(record))


# Attach handlers directly to this logger (instead of logging.basicConfig) so the file handler is added
# even if pytest or another plugin already configured root logging.
logger = logging.getLogger("Test")
logger.setLevel(logging.DEBUG)

if not logger.handlers:
    log_format = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    date_format = "%H:%M:%S"

    # File handler: every record (log calls *and* redirected prints) lands here.
    # The stream is opened line-buffered (buffering=1) so records are written to the .log
    # on each newline, instead of waiting for the block buffer to fill or a clean interpreter exit.
    file_handler = logging.FileHandler(_log_path, encoding="utf-8")
    file_handler.stream.close()  # close default buffered stream before replacing it
    file_handler.stream = open(file_handler.baseFilename, "a", encoding="utf-8", newline="", buffering=1)
    file_formatter_cls = ColorFormatter if _KEEP_COLORS_IN_FILE else PlainFormatter
    file_handler.setFormatter(file_formatter_cls(log_format, datefmt=date_format))
    logger.addHandler(file_handler)

    # Stream handler writes to the *real* stdout (sys.__stdout__), captured before we redirect
    # sys.stdout below. This echoes output on screen without recursing into the wrapper.
    # Colors are kept here: the level name gets colored and ANSI codes coming from pytest pass through.
    stream_handler = logging.StreamHandler(sys.__stdout__)
    console_formatter_cls = ColorFormatter if _stream_supports_color(sys.__stdout__) else logging.Formatter
    stream_handler.setFormatter(console_formatter_cls(log_format, datefmt=date_format))
    logger.addHandler(stream_handler)

logger.propagate = False


class _PrintToLogger:
    """Drop-in replacement for ``sys.stdout`` that routes every ``print()`` call
    through :data:`logger`, so terminal output is also captured in the log file.

    Writes are buffered and emitted as a single log record when a newline or a flush
    occurs, mimicking ``print()``'s line-based behaviour."""

    def __init__(self):
        self._buffer = []

    def write(self, message):
        if not message:
            return 0
        self._buffer.append(message)
        if "\n" in message:
            self.flush()
        return len(message)

    def flush(self):
        if self._buffer:
            text = "".join(self._buffer)
            self._buffer.clear()
            if _ANSI_RE.sub("", text).strip() == "":
                # Only control sequences (e.g. pytest's terminal progress bar): there is nothing to log,
                # so skip the log record and hand the sequence straight to a real terminal, if any.
                if sys.__stdout__.isatty():
                    sys.__stdout__.write(text)
            else:
                logger.info(text.rstrip("\n"))
        # Always forward flush to the real stdout (some libraries expect it).
        sys.__stdout__.flush()

    def isatty(self):
        # Keeps pytest (and other libs) emitting colors when the real terminal supports them.
        return sys.__stdout__.isatty()

    def __getattr__(self, name):
        return getattr(sys.__stdout__, name)


# Redirect stdout so every print() in the tests is logged too.
sys.stdout = _PrintToLogger()
sys.stderr = _PrintToLogger()

# Single shared logger instance for every test folder. Import it from any test:
#     from tests.libs.logger_setup import logger