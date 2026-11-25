import logging
import os
import sys
from datetime import datetime

# Single shared logger instance for every test folder. Import it from any test:
#     from src.app.core.logger_setup import logger


_libs_dir = os.path.dirname(os.path.abspath(__file__))
_root = os.path.dirname(os.path.dirname(_libs_dir))
_log_dir = os.path.join(_root, "app", "logs")
os.makedirs(_log_dir, exist_ok=True)
_log_path = os.path.join(_log_dir, f"app_run_{datetime.now():%Y%m%d_%H%M%S}.log")

# Attach handlers directly to this logger (instead of logging.basicConfig) so the file handler is added
# even if pytest or another plugin already configured root logging.
formatter = logging.Formatter("%(asctime)s | %(levelname)-8s | %(name)s | %(message)s", datefmt="%H:%M:%S")

logger = logging.getLogger("APP")
logger.setLevel(logging.DEBUG)

if not logger.handlers:
    # File handler: every record (log calls *and* redirected prints) lands here.
    # The stream is opened line-buffered (buffering=1) so records are written to the .log
    # on each newline, instead of waiting for the block buffer to fill or a clean interpreter exit.
    file_handler = logging.FileHandler(_log_path, encoding="utf-8")
    file_handler.stream.close()  # close default buffered stream before replacing it
    file_handler.stream = open(file_handler.baseFilename, "a", encoding="utf-8", newline="", buffering=1)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Stream handler writes to the *real* stdout (sys.__stdout__), captured before we redirect
    # sys.stdout below. This echoes output on screen without recursing into the wrapper.
    stream_handler = logging.StreamHandler(sys.__stdout__)
    stream_handler.setFormatter(formatter)
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
            logger.info(text.rstrip("\n"))
        # Always forward flush to the real stdout (some libraries expect it).
        sys.__stdout__.flush()

    def isatty(self):
        return sys.__stdout__.isatty()

    def __getattr__(self, name):
        return getattr(sys.__stdout__, name)


# Redirect stdout so every print() in the app is logged too.
sys.stdout = _PrintToLogger()
sys.stderr = _PrintToLogger()
