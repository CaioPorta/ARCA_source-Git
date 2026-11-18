from PyQt5.QtCore import Qt


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
        "'Análise do Mercado' button not found; expected to be on the not-logged-in home page."
    qtbot.mouseClick(window.Button_Mercado, Qt.LeftButton)
    assert window.PageID == '5', f"Expected the analysis page (PageID '5'), got '{window.PageID}'."

def go_back_page(window, qtbot):
    """
    Click the header return button to go back to the previous page.

    Pre-requisite: be on a page that shows the header (any page except the home page).
    """
    assert getattr(window, 'Button_Return', None) is not None, \
        "No return button available for this page."
    qtbot.mouseClick(window.Button_Return, Qt.LeftButton)