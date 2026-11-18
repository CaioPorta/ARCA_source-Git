import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%H:%M:%S",
)

# Single shared logger instance for every test folder. Import it from any test:
#     from tests.libs.logging_setup import logger
logger = logging.getLogger("tests")
