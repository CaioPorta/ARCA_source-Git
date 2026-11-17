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
