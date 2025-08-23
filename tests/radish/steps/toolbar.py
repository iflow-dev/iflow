"""
Step definitions for toolbar.
"""


from radish import when
from bdd.controls import Button
import time


@when("I click the refresh button in the toolbar")
def i_click_refresh_button_in_toolbar_new(step):
    refresh_button = Button("icon", None, "refresh-outline")
    refresh_button.click()

    # Wait a moment for the refresh to complete
    time.sleep(1)
