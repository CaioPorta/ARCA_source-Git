import pytest
from time import sleep

from PyQt5.QtWidgets import QApplication

from tests.libs.logging_setup import logger

import tests.libs.ui_helpers as ui

TIME_TO_VISUAL_CHECK = 1 # Seconds


def test_all_pages_are_correctly_loaded(window, assure_tester_account_exists, login, request: pytest.FixtureRequest):
    """
    Test that all pages are correctly loaded.
    """
    for_visual_check = request.config.getoption("--visual-check", default=False)
    window = ui.go_ARCA_page(window)
    assert window is not None
    if for_visual_check: sleep(TIME_TO_VISUAL_CHECK)

def test_launch_app_and_go_analise_go_back(window, qtbot, request: pytest.FixtureRequest):
    """
    Test that the app can be launched, go to the analysis page and go back to the main page.
    """
    for_visual_check = request.config.getoption("--visual-check", default=False)

    # The app is launched on the not-logged-in home page (PageID '0').
    assert window.PageID == '0'
    logger.info(f"App launched on home page (PageID={window.PageID}).")

    # Baseline: number of top-level windows present right after launch (just IHMmain's own widgets).
    baseline_windows = len(QApplication.topLevelWidgets())
    logger.info(f"Baseline top-level windows at launch: {baseline_windows}.")

    # Click "Análise do Mercado" to open the analysis tab.
    ui.go_Analise_without_login_page(window, qtbot)
    if for_visual_check: sleep(TIME_TO_VISUAL_CHECK)
    logger.info(f"Navigated to Análise do Mercado (PageID={window.PageID}).")

    # Regression guard: navigating must not leak extra top-level windows. The ClearPage bug detached
    # page widgets as visible top-level panels, roughly doubling the window count. Allow at most double
    # the baseline (the main app plus a small number of properly-closed widgets).
    current_windows = len(QApplication.topLevelWidgets())
    assert current_windows <= 2 * baseline_windows, (
        f"Analysis page leaked extra top-level windows: {current_windows} vs baseline {baseline_windows}. "
        f"Expected at most {2 * baseline_windows}."
    )

    # Return to the home page.
    ui.go_back_page(window, qtbot)
    if for_visual_check: sleep(TIME_TO_VISUAL_CHECK)
    logger.info(f"Returned to home page (PageID={window.PageID}).")

    assert window.PageID == '0'
    logger.info("Test passed: analysis page opened and returned home successfully.")
