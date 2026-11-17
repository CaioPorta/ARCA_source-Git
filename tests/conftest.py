import pytest
from PyQt5.QtCore import Qt

from ui.HMI import IHMmain
import tests.libs.ui_helpers as ui
# import os
# os.environ.setdefault("QT_QPA_PLATFORM", "offscreen") # Command to hide the GUI during tests.


@pytest.fixture(scope="session", autouse=True)
def window(qtbot):
    """
    Fixture to launch the application.
    """
    window = IHMmain()
    qtbot.addWidget(window)
    window.show()
    yield window

@pytest.fixture(scope="session", autouse=True)
def teardown():
    """
    Teardown function to clean up after tests.
    """
    ui.go_home()

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
