import os
import sys

import pytest
from _pytest.config import UsageError


def pytest_addoption(parser):
    parser.addoption(
        "--visual-check",
        action="store_true",
        default=False,
        help=(
            "Pause on screen between UI steps so you can follow the test flow visually."
        ),
    )
    parser.addoption(
        "--no-teardown",
        action="store_true",
        default=False,
        help=(
            "Keep the app window open on screen after the test for manual inspection instead of "
            "resetting/closing it. Only valid together with --visual-check and when a single test runs."
        ),
    )
    parser.addoption(
        "--use-official-db",
        action="store_true",
        default=False,
        help=(
            "Point the app at Users.db in the project root (like running ARCA.py from the repo root) "
            "instead of tests/test_output/Users.db. os.getcwd() is redirected to the project root; image "
            "loading keeps using src/assets."
        ),
    )


def pytest_configure(config):
    # Keeping the window open only makes sense while the GUI is actually shown on screen.
    if config.getoption("--no-teardown", default=False) and not config.getoption(
        "--visual-check", default=False
    ):
        raise UsageError("--no-teardown can only be used together with --visual-check.")


def pytest_collection_modifyitems(config, items):
    # The window stays open until closed manually, so this only makes sense for a single test.
    if config.getoption("--no-teardown", default=False) and len(items) != 1:
        raise UsageError(
            "--no-teardown can only be used when exactly one test runs, but "
            f"{len(items)} were selected."
        )


# The path to app UI.
_SRC_APP = os.path.join(os.path.dirname(__file__), "src", "app")
if _SRC_APP not in sys.path:
    sys.path.insert(0, _SRC_APP)

# The path to assets.
_DIST_DIR = os.path.join(os.path.dirname(__file__), "src", "assets")
if os.path.isdir(_DIST_DIR):
    os.chdir(_DIST_DIR)


@pytest.fixture(scope="session", autouse=True)
def official_db(request):
    # Tests run from src/assets so images load via relative ./images/... paths. Redirect os.getcwd()
    # to a dedicated DB directory instead, so Users.db never lands in src/assets by default.
    # --use-official-db points at the project root (like ARCA.py launched from the repo root).
    if request.config.getoption("--use-official-db", default=False):
        db_dir = os.path.dirname(os.path.abspath(__file__))
    else:
        db_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tests", "test_output")
    os.makedirs(db_dir, exist_ok=True)
    original_getcwd = os.getcwd
    os.getcwd = lambda: db_dir
    yield db_dir
    os.getcwd = original_getcwd
