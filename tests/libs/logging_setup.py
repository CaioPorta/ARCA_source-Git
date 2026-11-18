import logging
import os
from datetime import datetime


# Test logs are written next to the pytest-html reports (tests/test_output/logs/) with a timestamp in
# the filename, so they are easy to find after a run.
_libs_dir = os.path.dirname(os.path.abspath(__file__))          # .../ARCA_source-Git/tests/libs
_repo_root = os.path.dirname(os.path.dirname(_libs_dir))        # .../ARCA_source-Git
_log_dir = os.path.join(_repo_root, "tests", "test_output", "logs")
os.makedirs(_log_dir, exist_ok=True)
_log_path = os.path.join(_log_dir, f"test_run_{datetime.now():%Y%m%d_%H%M%S}.log")

# Attach handlers directly to this logger (instead of logging.basicConfig) so the file handler is added
# even if pytest or another plugin already configured root logging.
logger = logging.getLogger("tests")
logger.setLevel(logging.INFO)

if not logger.handlers:
    formatter = logging.Formatter("%(asctime)s | %(levelname)-8s | %(name)s | %(message)s", datefmt="%H:%M:%S")
    file_handler = logging.FileHandler(_log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

logger.propagate = False

# Single shared logger instance for every test folder. Import it from any test:
#     from tests.libs.logging_setup import logger
