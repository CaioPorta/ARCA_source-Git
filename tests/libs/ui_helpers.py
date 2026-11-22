import os

from PyQt5.QtCore import Qt, QTimer, QEventLoop
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QApplication

from ui.HMI import IHMmain

TIME_TO_VISUAL_CHECK = 1 # Seconds


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


def visual_sleep(for_visual_check=True, seconds=TIME_TO_VISUAL_CHECK):
    # Block while keeping the Qt event loop running so the window keeps repainting and stays visible
    # for the duration. time.sleep() freezes the loop, so the page blinks past instead of holding.
    if for_visual_check:
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
    Navigate to the ARCA page from the MinhaCarteira page (PageID '1').

    Pre-requisite: be on the MinhaCarteira page, where the 'ARCA' button lives.
    """
    assert getattr(window, 'Button_ARCA', None) is not None, \
        "'ARCA' button not found; expected to be on the MinhaCarteira page."
    _show_click(window.Button_ARCA)
    window.Button_ARCA.pressed.emit()
    return window

def go_Desempenho_page(window):
    """
    Navigate to the Desempenho page from the MinhaCarteira page (PageID '1').

    Pre-requisite: be on the MinhaCarteira page, where the 'Desempenho' button lives.
    """
    assert getattr(window, 'Button_Desempenho', None) is not None, \
        "'Desempenho' button not found; expected to be on the MinhaCarteira page."
    _show_click(window.Button_Desempenho)
    window.Button_Desempenho.pressed.emit()
    return window

def go_Mercado_page(window):
    """
    Navigate to the Análise do Mercado page from the MinhaCarteira page (PageID '1').

    Pre-requisite: be on the MinhaCarteira page, where the 'Análise do Mercado' button lives.
    """
    assert getattr(window, 'Button_Mercado', None) is not None, \
        "'Análise do Mercado' button not found; expected to be on the MinhaCarteira page."
    _show_click(window.Button_Mercado)
    window.Button_Mercado.pressed.emit()
    return window

def go_Trades_page(window):
    """
    Navigate to the Trades page (EdicaoNegociacoes, PageID '10') from the MinhaCarteira page (PageID '1').

    Pre-requisite: be on the MinhaCarteira page, where the 'Negociações' button lives.
    """
    window = go_Negociacoes_page(window)
    return window

def go_Trades_Bolsa_page(window):
    """
    Navigate to the EdicaoNegociacoesBolsa page (Trades -> Bolsa, PageID '18') from the MinhaCarteira page.

    Pre-requisite: be on the MinhaCarteira page. Navigates through the Trades page, then clicks the
    'Bolsa' button there.
    """
    window = go_Trades_page(window)
    assert getattr(window, 'Button_TradesBolsa', None) is not None, \
        "'Bolsa' button not found; expected to be on the Trades page."
    _show_click(window.Button_TradesBolsa)
    window.Button_TradesBolsa.pressed.emit()
    return window

def go_Trades_Criptomoedas_page(window):
    """
    Navigate to the EdicaoNegociacoesCripto page (Trades -> Criptomoedas, PageID '19') from the MinhaCarteira page.

    Pre-requisite: be on the MinhaCarteira page. Navigates through the Trades page, then clicks the
    'Criptomoedas' button there.
    """
    window = go_Trades_page(window)
    assert getattr(window, 'Button_TradesCriptomoedas', None) is not None, \
        "'Criptomoedas' button not found; expected to be on the Trades page."
    _show_click(window.Button_TradesCriptomoedas)
    window.Button_TradesCriptomoedas.pressed.emit()
    return window

def go_Tributacao_page(window):
    """
    Navigate to the Tributacao page from the MinhaCarteira page (PageID '1').

    Pre-requisite: be on the MinhaCarteira page, where the 'Tributacao' button lives.
    """
    assert getattr(window, 'Button_Tributacao', None) is not None, \
        "'Tributacao' button not found; expected to be on the MinhaCarteira page."
    _show_click(window.Button_Tributacao)
    window.Button_Tributacao.pressed.emit()
    return window

def go_Negociacoes_page(window):
    """
    Navigate to the EdicaoNegociacoes page from the MinhaCarteira page (PageID '1').

    Pre-requisite: be on the MinhaCarteira page, where the 'Negociações' button lives.
    """
    assert getattr(window, 'Button_Negociações', None) is not None, \
        "'Negociações' button not found; expected to be on the MinhaCarteira page."
    _show_click(window.Button_Negociações)
    window.Button_Negociações.pressed.emit()
    return window

def go_Perfil_page(window):
    """
    Navigate to the Perfil (auxiliary) page from any logged-in page via the header button.

    Pre-requisite: be on a logged-in page that shows the header, where the 'Perfil' button lives.
    """
    assert getattr(window, 'Button_Perfil', None) is not None, \
        "Perfil header button not found."
    _show_click(window.Button_Perfil)
    window.Button_Perfil.pressed.emit()
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
