import os
import sys
import pytest
from PyQt5.QtCore import QEventLoop, QTimer, Qt, qInstallMessageHandler
from PyQt5.QtWidgets import QApplication

from ui.HMI import IHMmain
import tests.libs.ui_helpers as ui

def _suppress_font_database_warning():
    # Headless (offscreen) Qt has no font directory, so it prints a spurious QFontDatabase warning.
    # Filter only that message; forward everything else to stderr so real warnings are not hidden.
    def _handler(message_type, context, message):
        if "QFontDatabase" in message or "Qt no longer ships fonts" in message:
            return
        sys.stderr.write(f"{message}\n")
        sys.stderr.flush()

    qInstallMessageHandler(_handler)


def pytest_configure(config):
    # Hide the GUI during normal test runs; reveal it on screen only when --visual-check is passed.
    if not config.getoption("--visual-check", default=False):
        os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")  # Run Qt headless unless visually checking.
        _suppress_font_database_warning()

    # pytest-html resolves --html relative to the current directory, but this project chdir's into
    # src/assets so the app can find its images. Force html output under tests/test_output/ instead.
    htmlpath = getattr(config.option, "htmlpath", None)
    if htmlpath:
        repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        out_dir = os.path.join(repo_root, "tests", "test_output")
        os.makedirs(out_dir, exist_ok=True)
        config.option.htmlpath = os.path.join(out_dir, os.path.basename(htmlpath))


@pytest.fixture(scope="function", autouse=True)
def window(qtbot, request: pytest.FixtureRequest):
    """
    Fixture to launch the application.
    """
    QApplication.setStyle("fusion")  # ARCA.py sets self.app.setStyle("fusion") before building widgets.
    window = IHMmain()
    window.initialize(check_version=False)  # initialize() shows the window maximized (HMI.py:113).
    QApplication.instance().processEvents()  # let showMaximized() and the maximized layout fully apply (real app runs app.exec_()).
    if not request.config.getoption("--no-teardown", default=False):
        qtbot.addWidget(window)  # Track the window so pytest-qt closes it at end of test. Skipped with --no-teardown.
    yield window

@pytest.fixture(scope="function", autouse=True)
def teardown(window, request):
    """
    Teardown function to clean up after tests: reset the window to the home page.
    With --no-teardown (only allowed with --visual-check for a single test), keep the window open
    on screen until it is closed manually instead of resetting it.

    Both branches must yield so pytest runs this fixture's body during setup and the code below
    during finalization (after the test). Without the yields pytest would run this body before the
    test, blocking on page 0 before the test body ever executes.
    """
    if request.config.getoption("--no-teardown", default=False):
        yield
        _wait_until_window_closed(window)
        return
    yield
    ui.go_home(window)


def _wait_until_window_closed(window):
    """Block the event loop, keeping the window visible and responsive until the user closes it."""
    loop = QEventLoop()
    timer = QTimer()
    timer.timeout.connect(lambda: (loop.quit() if not window.isVisible() else None))
    timer.start(200)
    window.show()
    window.raise_()
    window.activateWindow()
    loop.exec_()

@pytest.fixture(scope="function", autouse=False)
def login():
    """
    Fixture to log in to the application.
    """
    Email, NomeDeUsuario = "moreiraporta@gmail.com", "Caio_tester"
    yield Email, NomeDeUsuario

@pytest.fixture(scope="function", autouse=False)
def delete_users_db():
    """
    Helper function to delete the users.db file.
    Shall be called when argument "--delete-users-db" is passed to pytest.
    """
    pass

@pytest.fixture(scope="function", autouse=False)
def delete_tester_account():
    """
    Helper function to delete the tester account from the database.
    Shall be called when argument "--delete-tester-account" is passed to pytest.
    Shall be executed only if Users.db exists.
    """
    pass

@pytest.fixture(scope="function", autouse=False)
def assure_tester_account_exists():
    """
    Helper function to assure that the tester account exists in the database.
    Shall be called when argument "--assure-account-exists" is passed to pytest.
    """
    pass
