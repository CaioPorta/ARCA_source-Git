import pytest

from tests.libs.logging_setup import logger
import tests.libs.ui_helpers as ui
from ui.pages import PAGE_BY_NAME, PAGE_BY_ID

TIME_TO_VISUAL_CHECK = 1 # Seconds


def test_explore_parent_home_no_logging(window, qtbot, for_visual_check):
    """
    Test that the app can be launched, go to the analysis page and go back to the main page.
    """
    if for_visual_check: ui._visual_sleep(TIME_TO_VISUAL_CHECK)
    # <Action> Check preconditions <Action>
    # <Result> App is on "HOME" page <Result>
    expected_page = 'HOME'
    observed_page = PAGE_BY_ID[window.PageID].name
    assert observed_page == expected_page, f"Expected {expected_page} page, but got {observed_page} page."
    logger.info(f"App started on {observed_page} page.")

    # Non-regression check: always keep 1 window opened
    amount_of_windows = ui._count_main_windows()
    assert amount_of_windows == 1, f"Expected 1 window opened, but got {amount_of_windows}."

    # <Action> Click "Análise do Mercado" button <Action>
    # <Result> "AnaliseMercado" page shows up <Result>
    ui.go_Analise_without_login_page(window, qtbot)
    expected_page = 'AnaliseMercado'
    observed_page = PAGE_BY_ID[window.PageID].name
    logger.info(f"Navigated to {expected_page}.")
    if for_visual_check: ui._visual_sleep(TIME_TO_VISUAL_CHECK)
    assert observed_page == expected_page, f"Expected {expected_page} page, but got {observed_page} page."
    
    # <Action> Click "Return" button <Action>
    # <Result> "HOME" page shows up <Result>
    ui.go_previous_page(window, qtbot)
    expected_page = 'HOME'
    observed_page = PAGE_BY_ID[window.PageID].name
    if for_visual_check: ui._visual_sleep(TIME_TO_VISUAL_CHECK)
    assert observed_page == expected_page, f"Expected {expected_page} page, but got {observed_page} page."

    # <Action> Click "Esqueci a senha" button <Action>
    # <Result> "AuxilioSenha" page shows up <Result>
    ui.go_Esqueci_senha_without_login_page(window, qtbot)
    expected_page = 'AuxilioSenha'
    observed_page = PAGE_BY_ID[window.PageID].name
    logger.info(f"Navigated to {expected_page}.")
    if for_visual_check: ui._visual_sleep(TIME_TO_VISUAL_CHECK)
    assert observed_page == expected_page, f"Expected {expected_page} page, but got {observed_page} page."

    # <Action> Click "Return" button <Action>
    # <Result> "HOME" page shows up <Result>
    ui.go_previous_page(window, qtbot)
    expected_page = 'HOME'
    observed_page = PAGE_BY_ID[window.PageID].name
    if for_visual_check: ui._visual_sleep(TIME_TO_VISUAL_CHECK)
    assert observed_page == expected_page, f"Expected {expected_page} page, but got {observed_page} page."

    # <Action> Click "Importar usuario" button <Action>
    # <Result> "ImportarUsuario" page shows up <Result>
    ui.go_Importar_usuario_without_login_page(window, qtbot)
    expected_page = 'ImportarUsuario'
    observed_page = PAGE_BY_ID[window.PageID].name
    logger.info(f"Navigated to {expected_page}.")
    if for_visual_check: ui._visual_sleep(TIME_TO_VISUAL_CHECK)
    assert observed_page == expected_page, f"Expected {expected_page} page, but got {observed_page} page."

    # <Action> Click "Return" button <Action>
    # <Result> "HOME" page shows up <Result>
    ui.go_previous_page(window, qtbot)
    expected_page = 'HOME'
    observed_page = PAGE_BY_ID[window.PageID].name
    if for_visual_check: ui._visual_sleep(TIME_TO_VISUAL_CHECK)
    assert observed_page == expected_page, f"Expected {expected_page} page, but got {observed_page} page."

    # <Action> Click "Criar novo usuario" button <Action>
    # <Result> "CriarUsuario" page shows up <Result>
    ui.go_Criar_usuario_without_login_page(window, qtbot)
    expected_page = 'CriarUsuario'
    observed_page = PAGE_BY_ID[window.PageID].name
    logger.info(f"Navigated to {expected_page}.")
    if for_visual_check: ui._visual_sleep(TIME_TO_VISUAL_CHECK)
    assert observed_page == expected_page, f"Expected {expected_page} page, but got {observed_page} page."

    # <Action> Click "Return" button <Action>
    # <Result> "HOME" page shows up <Result>
    ui.go_previous_page(window, qtbot)
    expected_page = 'HOME'
    observed_page = PAGE_BY_ID[window.PageID].name
    if for_visual_check: ui._visual_sleep(TIME_TO_VISUAL_CHECK)
    assert observed_page == expected_page, f"Expected {expected_page} page, but got {observed_page} page."

    # Non-regression check: always keep 1 window opened
    amount_of_windows = ui._count_main_windows()
    assert amount_of_windows == 1, f"Expected 1 window opened, but got {amount_of_windows}."


def test_explore_parent_minha_carteira(window, assure_tester_account_exists, login, for_visual_check):
    """
    Test that all pages are correctly loaded.
    """
    if for_visual_check: ui._visual_sleep(TIME_TO_VISUAL_CHECK)
    # <Action> Check preconditions <Action>
    # <Result> App is on "MinhaCarteira" page <Result>
    expected_page = 'MinhaCarteira'
    observed_page = PAGE_BY_ID[window.PageID].name
    assert observed_page == expected_page, f"Expected {expected_page} page, but got {observed_page} page."
    logger.info(f"App started on {observed_page} page.")

    # <Action> Click "ARCA" button <Action>
    # <Result> "ARCA" page shows up <Result>

    # <Action> Click "Return" button <Action>
    # <Result> "MinhaCarteira" page shows up <Result>

    # <Action> Click "TODO" button <Action>
    # <Result> "CriarUsuario" page shows up <Result>

    # <Action> Click "Return" button <Action>
    # <Result> "MinhaCarteira" page shows up <Result>
    
    # <Action> Click "TODO" button <Action>
    # <Result> "CriarUsuario" page shows up <Result>

    # <Action> Click "Return" button <Action>
    # <Result> "MinhaCarteira" page shows up <Result>
    
    # <Action> Click "TODO" button <Action>
    # <Result> "CriarUsuario" page shows up <Result>

    # <Action> Click "Return" button <Action>
    # <Result> "MinhaCarteira" page shows up <Result>
    pass # TODO
