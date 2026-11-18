import pytest
from time import sleep

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

def test_launch_app_and_go_analise_go_back(window, request: pytest.FixtureRequest):
    """
    Test that the app can be launched, go to the analysis page and go back to the main page.
    """
    for_visual_check = request.config.getoption("--visual-check", default=False)
    window = ui.go_Analise_without_login_page(window)
    assert window is not None
    if for_visual_check: sleep(TIME_TO_VISUAL_CHECK)
    window = ui.go_back_page(window)
    assert window is not None
