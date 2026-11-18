import pytest

from tests.libs.logging_setup import logger
from tests.libs.ui_helpers import _count_main_windows, _visual_sleep
import tests.libs.ui_helpers as ui

TIME_TO_VISUAL_CHECK = 1 # Seconds


def test_explore_before_login(window, qtbot, request: pytest.FixtureRequest):
    """
    Test that the app can be launched, go to the analysis page and go back to the main page.
    """
    for_visual_check = request.config.getoption("--visual-check", default=False)

    # <Action> Check preconditions <Action>
    # <Result> App is on "page 0" <Result>
    if for_visual_check: ui._visual_sleep(TIME_TO_VISUAL_CHECK)
    # The app is launched on the not-logged-in home page (PageID '0').
    assert window.PageID == '0', f"Expected PageID '0' on launch, but got '{window.PageID}'."
    logger.info(f"App launched on home page (PageID={window.PageID}).")

    # Baseline: number of application main windows present right after launch (just IHMmain).
    baseline_windows = ui._count_main_windows()
    logger.info(f"Baseline main windows at launch: {baseline_windows}.")
    assert baseline_windows == 1, f"Expected 1 main window on launch, but got {baseline_windows}."

    # <Action> Click "Análise do Mercado" <Action>
    # <Result> "Análise do Mercado" page shows up <Result>
    ui.go_Analise_without_login_page(window, qtbot)
    logger.info(f"Navigated to Análise do Mercado (PageID={window.PageID}).")
    if for_visual_check: ui._visual_sleep(TIME_TO_VISUAL_CHECK)
    assert window.PageID == '5', f"Expected PageID '5' for Análise do Mercado page, but got '{window.PageID}'."

    # Regression guard: navigating must not open a second application main window.
    current_windows = ui._count_main_windows()
    assert current_windows == 1, (
        f"Analysis page opened extra main windows: {current_windows}. "
        f"Expected 1."
    )
    
    # <Action> Click "Return" button <Action>
    # <Result> "Page 0" shows up <Result>
    ui.go_back_page(window, qtbot)
    logger.info(f"Returned to home page (PageID={window.PageID}).")
    if for_visual_check: ui._visual_sleep(TIME_TO_VISUAL_CHECK)

    assert window.PageID == '0', f"Expected PageID '0' after returning, but got '{window.PageID}'."
    logger.info("Test passed: analysis page opened and returned home successfully.")

    # <Action> Click "Esqueci a senha" <Action>
    # <Result> "Esqueci a senha" page shows up <Result>

    # <Action> Click "Return" button <Action>
    # <Result> "Page 0" shows up <Result>

    # <Action> Click "Importar usuario" <Action>
    # <Result> "Importar usuario" page shows up <Result>

    # <Action> Click "Return" button <Action>
    # <Result> "Page 0" shows up <Result>

    # <Action> Click "Criar novo usuario" <Action>
    # <Result> "Criar novo usuario" page shows up <Result>

    # <Action> Click "Return" button <Action>
    # <Result> "Page 0" shows up <Result>


def test_all_pages_are_correctly_loaded(window, assure_tester_account_exists, login, request: pytest.FixtureRequest):
    """
    Test that all pages are correctly loaded.
    """
    pass # TODO