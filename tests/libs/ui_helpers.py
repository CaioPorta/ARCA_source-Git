import os

from PyQt5.QtCore import Qt, QTimer, QEventLoop
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QApplication

from ui.HMI import IHMmain


def _show_click(widget):
    # During visual checks (real screen) move the OS cursor to the widget center so the click is
    # visible. No-op under the headless offscreen Qt platform.
    if os.environ.get("QT_QPA_PLATFORM") == "offscreen":
        return
    QCursor.setPos(widget.mapToGlobal(widget.rect().center()))


def _count_main_windows():
    # topLevelWidgets() also returns orphaned home-page controls (parent=None), so count only the
    # real application main window(s) by class.
    return sum(1 for w in QApplication.topLevelWidgets() if isinstance(w, IHMmain))


def _visual_sleep(seconds):
    # Block while keeping the Qt event loop running so the window keeps repainting and stays visible
    # for the duration. time.sleep() freezes the loop, so the page blinks past instead of holding.
    loop = QEventLoop()
    timer = QTimer()
    timer.timeout.connect(loop.quit)
    timer.start(int(seconds * 1000))
    loop.exec_()


def go_home(window):
    """
    Ensure the window is on the not-logged-in home page (PageID '0').

    Called during teardown so each test starts from a known state. If the
    window ended up logged in somewhere else, log out to reach the home page.
    """
    if getattr(window, 'PageID', None) == '0':
        return window
    logout = getattr(window, 'Button_Sair', None)
    if logout is not None:
        logout.pressed.emit()
    return window

def go_ARCA_page(window):
    """
    Navigate to the ARCA page of the application.
    """
    window = go_home(window)
    pass # TODO
    return window

def go_Desempenho_page(window):
    """
    Navigate to the Desempenho page of the application.
    """
    window = go_home(window)
    pass # TODO
    return window

def go_Mercado_page(window):
    """
    Navigate to the Mercado page of the application.
    """
    window = go_home(window)
    pass # TODO
    return window

def go_Trades_page(window):
    """
    Navigate to the Trades page of the application.
    """
    window = go_home(window)
    pass # TODO
    return window

def go_Trades_Bolsa_page(window):
    """
    Navigate to the Trades Bolsa page of the application.
    """
    window = go_Trades_page(window)
    pass # TODO
    return window

def go_Trades_Criptomoedas_page(window):
    """
    Navigate to the Trades Criptomoedas page of the application.
    """
    window = go_Trades_page(window)
    pass # TODO
    return window

def go_Tributacao_page(window):
    """
    Navigate to the Tributacao page of the application.
    """
    window = go_home(window)
    pass # TODO
    return window

def go_Analise_without_login_page(window, qtbot):
    """
    From the not-logged-in home page (PageID '0'), open the "Análise do Mercado" tab.

    Pre-requisite: be on the not-logged-in home page (PageID '0').
    """
    assert getattr(window, 'Button_Mercado', None) is not None, \
        "'Análise do Mercado' button not found; expected to be on the page 0."
    _show_click(window.Button_Mercado)
    qtbot.mouseClick(window.Button_Mercado, Qt.LeftButton)

def go_Esqueci_senha_without_login_page(window, qtbot):
    """
    From the not-logged-in home page (PageID '0'), open the "Esqueci a senha" tab.

    Pre-requisite: be on the not-logged-in home page (PageID '0').
    """
    assert getattr(window, 'Button_EsqueciASenha', None) is not None, \
        "'Esqueci a senha' button not found; expected to be on the page 0."
    _show_click(window.Button_EsqueciASenha)
    qtbot.mouseClick(window.Button_EsqueciASenha, Qt.LeftButton)

def go_Importar_usuario_without_login_page(window, qtbot):
    """
    From the not-logged-in home page (PageID '0'), open the "Importar usuário" tab.

    Pre-requisite: be on the not-logged-in home page (PageID '0').
    """
    assert getattr(window, 'Button_ImportarUsuario', None) is not None, \
        "'Importar usuário' button not found; expected to be on the page 0."
    _show_click(window.Button_ImportarUsuario)
    qtbot.mouseClick(window.Button_ImportarUsuario, Qt.LeftButton)

def go_Criar_usuario_without_login_page(window, qtbot):
    """
    From the not-logged-in home page (PageID '0'), open the "Criar novo usuário" tab.

    Pre-requisite: be on the not-logged-in home page (PageID '0').
    """
    assert getattr(window, 'Button_CriarUsuario', None) is not None, \
        "'Criar novo usuário' button not found; expected to be on the page 0."
    _show_click(window.Button_CriarUsuario)
    qtbot.mouseClick(window.Button_CriarUsuario, Qt.LeftButton)

def go_previous_page(window, qtbot):
    """
    Click the header return button to go back to the previous page.

    Pre-requisite: be on a page that shows the header (any page except the home page).
    """
    assert getattr(window, 'Button_Return', None) is not None, \
        "No return button available for this page."
    _show_click(window.Button_Return)
    qtbot.mouseClick(window.Button_Return, Qt.LeftButton)