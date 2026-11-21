import pytestqt
from tests.libs.logging_setup import logger
import os
import sys
import pytest
import toml
import sqlite3
from PyQt5.QtCore import QEventLoop, QTimer, Qt, qInstallMessageHandler
from PyQt5.QtWidgets import QApplication

from ui.HMI import IHMmain
import tests.libs.ui_helpers as ui
from ui.pages import PAGE_BY_ID

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


@pytest.fixture(scope="function", autouse=True)
def window(qtbot, request: pytest.FixtureRequest) -> IHMmain:
    """
    Fixture to launch the application.
    """
    QApplication.setStyle("fusion")  # ARCA.py sets self.app.setStyle("fusion") before building widgets.
    window = IHMmain()
    window.initialize(check_version=False)  # initialize() shows the window maximized (HMI.py:113).
    QApplication.instance().processEvents()  # let showMaximized() and the maximized layout fully apply (real app runs app.exec_()).
    if not request.config.getoption("--no-teardown", default=False):
        qtbot.addWidget(window)  # Track the window so pytest-qt closes it at end of test. Skipped with --no-teardown.
    return window

@pytest.fixture(scope="function", autouse=True)
def teardown(window, request) -> None:
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

@pytest.fixture(scope="session", autouse=True)
def for_visual_check(request: pytest.FixtureRequest) -> bool:
    return request.config.getoption("--visual-check", default=False)

@pytest.fixture(scope="function", autouse=False)
def login(user_info, window, qtbot, for_visual_check) -> tuple[str, str, str]:
    """
    Fixture to log in to the application.
    Ensures the tester account exists and authenticates through the UI, landing on the logged-in
    MinaCarteira page so tests can explore the authenticated workflow.
    """
    NomeDeUsuario, Senha, Email = user_info
    
    expected_page = 'Home'
    observed_page = PAGE_BY_ID[window.PageID].name
    assert observed_page == expected_page, f"Expected {expected_page} page, but got {observed_page} page."
    logger.info(f"[OK] App started on {observed_page} page.")
    for attr in ('TextBox_NomeDeUsuario', 'TextBox_Senha', 'Button_LogIn'):
        assert getattr(window, attr, None) is not None, \
            f"'{attr}' not found; expected the home/login page."
    window.TextBox_NomeDeUsuario.setText(NomeDeUsuario)
    window.TextBox_Senha.setText(Senha)
    ui.visual_sleep(for_visual_check)
    qtbot.mouseClick(window.Button_LogIn, Qt.LeftButton)
    yield NomeDeUsuario, Senha, Email

@pytest.fixture(scope="function", autouse=False)
def delete_users_db() -> None:
    """
    Helper function to delete the users.db file.
    """
    pass

def delete_account(user: str, password: str, email: str) -> None:
    """
    Helper function to delete the tester account from the database.
    Shall be executed only if Users.db exists.
    """
    pass

@pytest.fixture(scope="function", autouse=False)
def assure_account_exists(user_info) -> None:
    """
    Helper function to assure that the tester account exists in the database.
    Shall be called when argument "--assure-account-exists" is passed to pytest.
    """
    """
    Create a minimal tester account (Users.db + per-user db) when it does not already exist, so the
    app can authenticate during tests. Uses os.getcwd() -- redirected to tests/test_output by the
    session fixture -- as both the Users.db location and the user's Path, which keeps logout's
    Disconnect() from deleting the account (it only removes the db when Path differs from cwd).
    """
    user, password, email = user_info
    cwd = os.getcwd()
    users_db = os.path.join(cwd, "Users.db")
    if not os.path.exists(users_db):
        conn = sqlite3.connect(users_db)
        conn.execute("CREATE TABLE IF NOT EXISTS 'Usuários' ('Usuário' TEXT, 'Email' TEXT, 'Path' TEXT)")
        conn.execute(
            "INSERT INTO 'Usuários' ('Usuário', 'Email', 'Path') VALUES (?, ?, ?)",
            (user, email, cwd),
        )
        conn.commit()
        conn.close()

    user_db = os.path.join(cwd, user + ".db")
    if not os.path.exists(user_db):
        conn = sqlite3.connect(user_db)
        conn.execute(
            "CREATE TABLE IF NOT EXISTS 'Perfil' "
            "('Usuário' TEXT, 'Senha' TEXT, 'Email' TEXT, 'TaxaB3Per' REAL, "
            "'MoedaCorrente' TEXT, 'GastoMensal' REAL, 'MesesDeReserva' REAL)"
        )
        conn.execute(
            "INSERT INTO 'Perfil' ('Usuário', 'Senha', 'Email', 'TaxaB3Per', 'MoedaCorrente', 'GastoMensal', 'MesesDeReserva') "
            "VALUES (?, ?, ?, 0.03, 'BRL', 0, 6)",
            (user, password, email),
        )
        conn.commit()
        conn.close()
    yield
    # delete_account(user, password, email)

@pytest.fixture(scope="function", autouse=False)
def user_info(request: pytest.FixtureRequest) -> tuple[str, str, str]:
    """
    A fixture to get from tests/login_tester.toml or from tests/login_official.toml the user, password and email.
    Depends on --use-official-db.
    """
    if request.config.getoption("--use-official-db", default=False):
        # Load official user info from tests/login_official.toml.
        login_file = os.path.join(os.path.dirname(__file__), "login_official.toml")
        with open(login_file, "r") as f:
            login_data = toml.load(f)
        NomeDeUsuario = login_data["USER"]
        Senha = login_data["PASSWORD"]
        Email = login_data["EMAIL"]
    else:
        # Load tester user info from tests/login_tester.toml.
        login_file = os.path.join(os.path.dirname(__file__), "login_tester.toml")
        with open(login_file, "r") as f:
            login_data = toml.load(f)
        NomeDeUsuario = login_data["USER"]
        Senha = login_data["PASSWORD"]
        Email = login_data["EMAIL"]
    return NomeDeUsuario, Senha, Email
