import os
import pytest
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from ui.HMI import IHMmain
import tests.libs.ui_helpers as ui

def pytest_configure(config):
    # Hide the GUI during normal test runs; reveal it on screen only when --visual-check is passed.
    if not config.getoption("--visual-check", default=False):
        os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")  # Run Qt headless unless visually checking.

    # pytest-html resolves --html relative to the current directory, but this project chdir's into
    # src/assets so the app can find its images. Force html output under tests/test_output/ instead.
    htmlpath = getattr(config.option, "htmlpath", None)
    if htmlpath:
        repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        out_dir = os.path.join(repo_root, "tests", "test_output")
        os.makedirs(out_dir, exist_ok=True)
        config.option.htmlpath = os.path.join(out_dir, os.path.basename(htmlpath))


@pytest.fixture(scope="function", autouse=True)
def window(qtbot):
    """
    Fixture to launch the application.
    """
    QApplication.setStyle("fusion")  # ARCA.py sets self.app.setStyle("fusion") before building widgets.
    window = IHMmain()
    window.initialize(check_version=False)  # initialize() shows the window maximized (HMI.py:113).
    QApplication.instance().processEvents()  # let showMaximized() and the maximized layout fully apply (real app runs app.exec_()).
    qtbot.addWidget(window)
    yield window

@pytest.fixture(scope="function", autouse=True)
def teardown(window):
    """
    Teardown function to clean up after tests: reset the window to the home page.
    """
    ui.go_home(window)

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
