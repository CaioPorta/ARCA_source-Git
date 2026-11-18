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


# HMI.py imports the app using top-level packages (core.*, ui.*), so src/app must
# be importable. Add it to sys.path so tests run without setting PYTHONPATH manually.
_SRC_APP = os.path.join(os.path.dirname(__file__), "src", "app")
if _SRC_APP not in sys.path:
    sys.path.insert(0, _SRC_APP)
