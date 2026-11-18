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

    # Click "Análise do Mercado" to open the analysis tab.
    ui.go_Analise_without_login_page(window, qtbot)
    if for_visual_check: sleep(TIME_TO_VISUAL_CHECK)
    logger.info(f"Navigated to Análise do Mercado (PageID={window.PageID}).")

    # Only the main app window should be visible; no leaked/extra top-level panels may remain open.
    visible_windows = [w for w in QApplication.topLevelWidgets() if w.isVisible()]
    assert len(visible_windows) == 1, (
        f"Expected exactly 1 visible top-level window (the main app), "
        f"found {len(visible_windows)}: {[type(w).__name__ for w in visible_windows]}"
    )

    # Return to the home page.
    ui.go_back_page(window, qtbot)
    if for_visual_check: sleep(TIME_TO_VISUAL_CHECK)
    logger.info(f"Returned to home page (PageID={window.PageID}).")

    assert window.PageID == '0'
    logger.info("Test passed: analysis page opened and returned home successfully.")
