import pytest
from time import sleep

from PyQt5.QtWidgets import QApplication

from ui.HMI import IHMmain

from tests.libs.logging_setup import logger

import tests.libs.ui_helpers as ui

TIME_TO_VISUAL_CHECK = 1 # Seconds


def _count_main_windows():
    # topLevelWidgets() also returns orphaned home-page controls (parent=None), so count only the
    # real application main window(s) by class.
    return sum(1 for w in QApplication.topLevelWidgets() if isinstance(w, IHMmain))


def test_all_pages_are_correctly_loaded(window, assure_tester_account_exists, login, request: pytest.FixtureRequest):
    """
    Test that all pages are correctly loaded.
    """
    pass # TODO

def test_launch_app_and_go_analise_go_back(window, qtbot, request: pytest.FixtureRequest):
    """
    Test that the app can be launched, go to the analysis page and go back to the main page.
    """
    for_visual_check = request.config.getoption("--visual-check", default=False)

    # The app is launched on the not-logged-in home page (PageID '0').
    assert window.PageID == '0', f"Expected PageID '0' on launch, but got '{window.PageID}'."
    logger.info(f"App launched on home page (PageID={window.PageID}).")

    # Baseline: number of application main windows present right after launch (just IHMmain).
    baseline_windows = _count_main_windows()
    logger.info(f"Baseline main windows at launch: {baseline_windows}.")
    assert baseline_windows == 1, f"Expected 1 main window on launch, but got {baseline_windows}."

    # Click "Análise do Mercado" to open the analysis tab.
    ui.go_Analise_without_login_page(window, qtbot)
    assert window.PageID == '5', f"Expected PageID '5' for Análise do Mercado page, but got '{window.PageID}'."
    if for_visual_check: sleep(TIME_TO_VISUAL_CHECK)
    logger.info(f"Navigated to Análise do Mercado (PageID={window.PageID}).")

    # Regression guard: navigating must not open a second application main window.
    current_windows = _count_main_windows()
    assert current_windows == 1, (
        f"Analysis page opened extra main windows: {current_windows}. "
        f"Expected 1."
    )
