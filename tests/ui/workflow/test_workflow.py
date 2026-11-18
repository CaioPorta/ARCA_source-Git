import pytest

from tests.libs.logging_setup import logger
from tests.libs.ui_helpers import _count_main_windows, _visual_sleep
import tests.libs.ui_helpers as ui

TIME_TO_VISUAL_CHECK = 1 # Seconds


def test_explore_before_login(window, qtbot, for_visual_check):
    """
    Test that the app can be launched, go to the analysis page and go back to the main page.
    """
    if for_visual_check: ui._visual_sleep(TIME_TO_VISUAL_CHECK)
    # <Action> Check preconditions <Action>
    # <Result> App is on "page 0" <Result>
    assert window.PageID == '0', f"Expected PageID '0' on launch, but got '{window.PageID}'."
    logger.info(f"App launched on home page (PageID={window.PageID}).")

    # Non-regression check: always keep 1 window opened
    amount_of_windows = ui._count_main_windows()
    assert amount_of_windows == 1, f"Expected 1 window opened, but got {amount_of_windows}."

    # <Action> Click "Análise do Mercado" button <Action>
    # <Result> "Análise do Mercado" page shows up <Result>
    ui.go_Analise_without_login_page(window, qtbot)
    logger.info(f"Navigated to Análise do Mercado (PageID={window.PageID}).")
    if for_visual_check: ui._visual_sleep(TIME_TO_VISUAL_CHECK)
    assert window.PageID == '5', f"Expected PageID '5' for Análise do Mercado page, but got '{window.PageID}'."
    
    # <Action> Click "Return" button <Action>
    # <Result> "Page 0" shows up <Result>
    ui.go_previous_page(window, qtbot)
    logger.info(f"Returned to home page (PageID={window.PageID}).")
    if for_visual_check: ui._visual_sleep(TIME_TO_VISUAL_CHECK)

    assert window.PageID == '0', f"Expected PageID '0' after returning, but got '{window.PageID}'."

    # <Action> Click "Esqueci a senha" button <Action>
    # <Result> "Esqueci a senha" page shows up <Result>
    ui.go_Esqueci_senha_without_login_page(window, qtbot)
    logger.info(f"Navigated to Esqueci a senha (PageID={window.PageID}).")
    if for_visual_check: ui._visual_sleep(TIME_TO_VISUAL_CHECK)

    # <Action> Click "Return" button <Action>
    # <Result> "Page 0" shows up <Result>
    ui.go_previous_page(window, qtbot)
    logger.info(f"Returned to home page (PageID={window.PageID}).")
    if for_visual_check: ui._visual_sleep(TIME_TO_VISUAL_CHECK)
    assert window.PageID == '0', f"Expected PageID '0' after returning, but got '{window.PageID}'."

    # <Action> Click "Importar usuario" button <Action>
    # <Result> "Importar usuario" page shows up <Result>
    ui.go_Importar_usuario_without_login_page(window, qtbot)
    logger.info(f"Navigated to Importar usuario (PageID={window.PageID}).")
    if for_visual_check: ui._visual_sleep(TIME_TO_VISUAL_CHECK)

    # <Action> Click "Return" button <Action>
    # <Result> "Page 0" shows up <Result>
    ui.go_previous_page(window, qtbot)
    logger.info(f"Returned to home page (PageID={window.PageID}).")
    if for_visual_check: ui._visual_sleep(TIME_TO_VISUAL_CHECK)
    assert window.PageID == '0', f"Expected PageID '0' after returning, but got '{window.PageID}'."

    # <Action> Click "Criar novo usuario" button <Action>
    # <Result> "Criar novo usuario" page shows up <Result>
    ui.go_Criar_usuario_without_login_page(window, qtbot)
    logger.info(f"Navigated to Criar novo usuario (PageID={window.PageID}).")
    if for_visual_check: ui._visual_sleep(TIME_TO_VISUAL_CHECK)

    # <Action> Click "Return" button <Action>
    # <Result> "Page 0" shows up <Result>
    ui.go_previous_page(window, qtbot)
    logger.info(f"Returned to home page (PageID={window.PageID}).")
    if for_visual_check: ui._visual_sleep(TIME_TO_VISUAL_CHECK)
    assert window.PageID == '0', f"Expected PageID '0' after returning, but got '{window.PageID}'."

    # Non-regression check: always keep 1 window opened
    amount_of_windows = ui._count_main_windows()
    assert amount_of_windows == 1, f"Expected 1 window opened, but got {amount_of_windows}."


def test_explore_arca(window, assure_tester_account_exists, login, request: pytest.FixtureRequest):
    """
    Test that all pages are correctly loaded.
    """
    # <Action> Click "ARCA" button <Action>
    # <Result> "Criar novo usuario" page shows up <Result>

    # <Action> Click "Return" button <Action>
    # <Result> "Page 0" shows up <Result>
    pass # TODO