from tests.libs.logger_setup import logger
import tests.libs.ui_helpers as ui
from ui.pages import PAGE_BY_ID


def test_explore_parent_home_no_logging(window, qtbot, for_visual_check):
    """
    Test that the app can be launched, go to the analysis page and go back to the main page.
    """
    ui.visual_sleep(for_visual_check)
    # <Action> Check preconditions <Action>
    # <Result> App is on "Home" page <Result>
    expected_page = 'Home'
    observed_page = PAGE_BY_ID[window.PageID].name
    assert observed_page == expected_page, f"Expected {expected_page} page, but got {observed_page} page."
    logger.info(f"[OK] App started on {observed_page} page.")

    # Non-regression check: always keep 1 window opened
    amount_of_windows = ui._count_main_windows()
    assert amount_of_windows == 1, f"Expected 1 window opened, but got {amount_of_windows}."

    # <Action> Click "Análise do Mercado" button <Action>
    # <Result> "AnaliseMercado" page shows up <Result>
    expected_page = 'AnaliseMercado'
    ui.go_Analise_without_login_page(window, qtbot, for_visual_check)

    # <Action> Click "Return" button <Action>
    # <Result> "Home" page shows up <Result>
    expected_page = 'Home'
    ui.go_previous_page(window, qtbot, for_visual_check, expected_page)

    # <Action> Click "Esqueci a senha" button <Action>
    # <Result> "AuxilioSenha" page shows up <Result>
    expected_page = 'AuxilioSenha'
    ui.go_Esqueci_senha_without_login_page(window, qtbot, for_visual_check)
    
    # <Action> Click "Return" button <Action>
    # <Result> "Home" page shows up <Result>
    expected_page = 'Home'
    ui.go_previous_page(window, qtbot, for_visual_check, expected_page)
    
    # <Action> Click "Importar usuario" button <Action>
    # <Result> "ImportarUsuario" page shows up <Result>
    expected_page = 'ImportarUsuario'
    ui.go_Importar_usuario_without_login_page(window, qtbot, for_visual_check)
    
    # <Action> Click "Return" button <Action>
    # <Result> "Home" page shows up <Result>
    expected_page = 'Home'
    ui.go_previous_page(window, qtbot, for_visual_check, expected_page)
    
    # <Action> Click "Criar novo usuario" button <Action>
    # <Result> "CriarUsuario" page shows up <Result>
    expected_page = 'CriarUsuario'
    ui.go_Criar_usuario_without_login_page(window, qtbot, for_visual_check)
    
    # <Action> Click "Return" button <Action>
    # <Result> "Home" page shows up <Result>
    expected_page = 'Home'
    ui.go_previous_page(window, qtbot, for_visual_check, expected_page)
    
    # Non-regression check: always keep 1 window opened
    amount_of_windows = ui._count_main_windows()
    assert amount_of_windows == 1, f"Expected 1 window opened, but got {amount_of_windows}."

def test_login(window, for_visual_check, assure_account_exists, login):
    """
    Test that all pages are correctly loaded.
    """
    ui.visual_sleep(for_visual_check)
    # <Action> Check preconditions <Action>
    # <Result> App is on "MinhaCarteira" page <Result>
    expected_page = 'MinhaCarteira'
    observed_page = PAGE_BY_ID[window.PageID].name
    assert observed_page == expected_page, f"Expected {expected_page} page, but got {observed_page} page."
    logger.info(f"[OK] App started on {observed_page} page.")

def test_explore_parent_minha_carteira(window, qtbot, for_visual_check, assure_account_exists, login):
    """
    Test that all pages directly under MinhaCarteira are correctly loaded.
    """
    ui.visual_sleep(for_visual_check)
    # <Action> Check preconditions <Action>
    # <Result> App is on "MinhaCarteira" page <Result>
    expected_page = 'MinhaCarteira'
    observed_page = PAGE_BY_ID[window.PageID].name
    assert observed_page == expected_page, f"Expected {expected_page} page, but got {observed_page} page."
    logger.info(f"[OK] App started on {observed_page} page.")

    # <Action> Click "Negociações" button <Action>
    # <Result> "EdicaoNegociacoes" page shows up <Result>
    ui.go_Negociacoes_page(window, qtbot, for_visual_check)

    # <Action> Click "Return" button <Action>
    # <Result> "MinhaCarteira" page shows up <Result>
    expected_page = 'MinhaCarteira'
    ui.go_previous_page(window, qtbot, for_visual_check, expected_page)

    # <Action> Click "ARCA" button <Action>
    # <Result> "ARCA" page shows up <Result>
    ui.go_ARCA_page(window, qtbot, for_visual_check)

    # <Action> Click "Return" button <Action>
    # <Result> "MinhaCarteira" page shows up <Result>
    expected_page = 'MinhaCarteira'
    ui.go_previous_page(window, qtbot, for_visual_check, expected_page)

    # <Action> Click "Tributacao" button <Action>
    # <Result> "Tributacao" page shows up <Result>
    ui.go_Tributacao_page(window, qtbot, for_visual_check)

    # <Action> Click "Return" button <Action>
    # <Result> "MinhaCarteira" page shows up <Result>
    expected_page = 'MinhaCarteira'
    ui.go_previous_page(window, qtbot, for_visual_check, expected_page)

    # <Action> Click "Desempenho" button <Action>
    # <Result> "Desempenho" page shows up <Result>
    # ui.go_Desempenho_page(window, qtbot, for_visual_check)

    # <Action> Click "Return" button <Action>
    # <Result> "MinhaCarteira" page shows up <Result>
    # expected_page = 'MinhaCarteira'
    # ui.go_previous_page(window, qtbot, for_visual_check, expected_page)

    # <Action> Click "Análise do Mercado" button <Action>
    # <Result> "AnaliseMercadoDup" page shows up <Result>
    ui.go_MercadoDup_page(window, qtbot, for_visual_check)

    # <Action> Click "Return" button <Action>
    # <Result> "MinhaCarteira" page shows up <Result>
    expected_page = 'MinhaCarteira'
    ui.go_previous_page(window, qtbot, for_visual_check, expected_page)

    # <Action> Click "Perfil" header button <Action>
    # <Result> "Perfil" (aux) page shows up <Result>
    ui.go_Perfil_page(window, qtbot, for_visual_check)

    # <Action> Click "Return" button <Action>
    # <Result> "MinhaCarteira" page shows up <Result>
    expected_page = 'MinhaCarteira'
    ui.go_previous_page(window, qtbot, for_visual_check, expected_page)

    # Non-regression check: always keep 1 window opened
    amount_of_windows = ui._count_main_windows()
    assert amount_of_windows == 1, f"Expected 1 window opened, but got {amount_of_windows}."

def test_trades_bolsa(window, qtbot, for_visual_check, assure_account_exists, login):
    """
    Test that the Trades -> Bolsa page is correctly loaded.
    """
    ui.visual_sleep(for_visual_check)
    # <Action> Check preconditions <Action>
    # <Result> App is on "MinhaCarteira" page <Result>
    expected_page = 'MinhaCarteira'
    observed_page = PAGE_BY_ID[window.PageID].name
    assert observed_page == expected_page, f"Expected {expected_page} page, but got {observed_page} page."
    logger.info(f"[OK] App started on {observed_page} page.")

    # <Action> Click "Negociações" button (via the Trades page) <Action>
    # <Result> "EdicaoNegociacoes" page shows up <Result>
    expected_page = 'EdicaoNegociacoes'
    ui.go_Trades_page(window, qtbot, for_visual_check)

    # <Action> Click "Bolsa" button (via the Trades page) <Action>
    # <Result> "EdicaoNegociacoesBolsa" page shows up <Result>
    expected_page = 'EdicaoNegociacoesBolsa'
    ui.go_Trades_Bolsa_page(window, qtbot, for_visual_check)

    # <Action> Click "Return" button <Action>
    # <Result> "EdicaoNegociacoes" (Trades) page shows up <Result>
    expected_page = 'EdicaoNegociacoes'
    ui.go_previous_page(window, qtbot, for_visual_check, expected_page)
    
    # Non-regression check: always keep 1 window opened
    amount_of_windows = ui._count_main_windows()
    assert amount_of_windows == 1, f"Expected 1 window opened, but got {amount_of_windows}."

def test_trades_criptomoedas(window, qtbot, for_visual_check, assure_account_exists, login):
    """
    Test that the Trades -> Criptomoedas page is correctly loaded.
    """
    ui.visual_sleep(for_visual_check)
    # <Action> Check preconditions <Action>
    # <Result> App is on "MinhaCarteira" page <Result>
    expected_page = 'MinhaCarteira'
    observed_page = PAGE_BY_ID[window.PageID].name
    assert observed_page == expected_page, f"Expected {expected_page} page, but got {observed_page} page."
    logger.info(f"[OK] App started on {observed_page} page.")

    # <Action> Click "EdicaoNegociacoes" button <Action>
    # <Result> "EdicaoNegociacoes" (Trades) page shows up <Result>
    expected_page = 'EdicaoNegociacoes'
    ui.go_Negociacoes_page(window, qtbot, for_visual_check)

    # <Action> Click "Criptomoedas" button (via the Trades page) <Action>
    # <Result> "EdicaoNegociacoesCripto" page shows up <Result>
    ui.go_Trades_Criptomoedas_page(window, qtbot, for_visual_check)

    # <Action> Click "Return" button <Action>
    # <Result> "EdicaoNegociacoes" (Trades) page shows up <Result>
    expected_page = 'EdicaoNegociacoes'
    ui.go_previous_page(window, qtbot, for_visual_check, expected_page)

    # <Action> Click "Return" button <Action>
    # <Result> "MinhaCarteira" (Trades) page shows up <Result>
    expected_page = 'MinhaCarteira'
    ui.go_previous_page(window, qtbot, for_visual_check, expected_page)

    # Non-regression check: always keep 1 window opened
    amount_of_windows = ui._count_main_windows()
    assert amount_of_windows == 1, f"Expected 1 window opened, but got {amount_of_windows}."
