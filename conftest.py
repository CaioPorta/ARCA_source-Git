import os
import sys


def pytest_addoption(parser):
    parser.addoption(
        "--visual-check",
        action="store_true",
        default=False,
        help=(
            "Pause on screen between UI steps so you can follow the test flow visually."
        ),
    )


# The path to app UI.
_SRC_APP = os.path.join(os.path.dirname(__file__), "src", "app")
if _SRC_APP not in sys.path:
    sys.path.insert(0, _SRC_APP)

# The path to assets.
_DIST_DIR = os.path.join(os.path.dirname(__file__), "src", "assets")
if os.path.isdir(_DIST_DIR):
    os.chdir(_DIST_DIR)
