"""
Basic step definitions.

Rule: driver handling
    - All users of the selenium web driver shall use it
      through direct import and access of world.driver
    - Driver instances may not be passed around through arguments
"""

from radish import given, when, then, step, world
from selenium.webdriver.common.by import By
from bdd.controls import Title, Button
from bdd.controls.page import Page
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from bdd.logging_config import logger as log



@given("I go to home")
def i_go_to_home(step):
    """Navigate to the home page (base URL)."""

    assert world.config.dry_run is False, "DRY_RUN.. test aborted"

    base_url = world.base_url
    world.driver.get(base_url)
    
    # Clear any open modals after navigation to ensure clean state
    page = Page()
    page.clear_modal()
    
    time.sleep(1)

    # check the driver url after navigation (allow for redirects)
    assert base_url in world.driver.current_url
    

@step("I am on the main page")
def i_am_on_main_page(step):
    """Check that we are on the main page (expects previous step to have navigated)."""
    title = Title("iflow")
    title.locate()

@when("I click the {button_text:QuotedString} button")
def i_click_button(step, button_text):
    """Click a button with the specified text."""
    button = Button("button", button_text, None)
    button.click()

@then("the page title should be displayed")
def page_title_should_be_displayed(step):
    """Verify the page title is displayed."""
    title = Title("iflow")
    title.locate()

@then("the artifact creation modal should be open")
def artifact_creation_modal_should_be_open(step):
    """
    Verify that the artifact creation modal is open.
    """
    wait = WebDriverWait(world.driver, 10)
    modal = wait.until(
        EC.visibility_of_element_located((By.ID, "artifactModal"))
    )
    assert modal.is_displayed(), "Artifact creation modal is not displayed"
