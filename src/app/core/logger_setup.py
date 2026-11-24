import logging
import os
import sys
from datetime import datetime

# Single shared logger instance for every test folder. Import it from any test:
#     from src.app.core.logger_setup import logger


_libs_dir = os.path.dirname(os.path.abspath(__file__))
_root = os.path.dirname(os.path.dirname(_libs_dir))
_log_dir = os.path.join(_root, "src", "app", "logs")
os.makedirs(_log_dir, exist_ok=True)
_log_path = os.path.join(_log_dir, f"app_run_{datetime.now():%Y%m%d_%H%M%S}.log")

# Attach handlers directly to this logger (instead of logging.basicConfig) so the file handler is added
# even if pytest or another plugin already configured root logging.
logger = logging.getLogger("app_log")
logger.setLevel(logging.INFO)

if not logger.handlers:
    formatter = logging.Formatter("%(asctime)s | %(levelname)-8s | %(name)s | %(message)s", datefmt="%H:%M:%S")
    file_handler = logging.FileHandler(_log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

logger.propagate = False

