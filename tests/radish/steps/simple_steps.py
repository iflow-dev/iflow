"""
Simple step definitions for basic functionality testing.
"""

from radish import given, when, then, step, world
from selenium.webdriver.common.by import By
from controls import Title, Button
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import logging_config  # Use the custom TRACE level

log = logging_config.logger

def _preinit():
    # Set base URL for the application
    base_url = os.getenv('IFLOW_BASE_URL')
    if not base_url:
        log.trace("IFLOW_BASE_URL environment variable not set")
        raise ValueError("IFLOW_BASE_URL environment variable must be set")
    log.trace(f"Testing against: {base_url}")
    
    # Store base URL directly in world object for easy access
    world.base_url = base_url
    world.driver = None
    log.trace(f"Base URL set in world: {world.base_url}")
    

def _init_driver():
    if hasattr(world, 'driver') and world.driver is not None:
        return
    
    _preinit()

    # Always use log.trace; custom TRACE level assumed to exist
    log.trace("Initializing Chrome driver for entire test session...")
    chrome_options = Options()
    
    # Check if headless mode should be disabled
    headless_mode = os.environ.get("HEADLESS_MODE", "true").lower() == "true"
    if headless_mode:
        chrome_options.add_argument("--headless")
        log.trace("Chrome running in headless mode")
    else:
        log.trace("Chrome running in visible mode (headless disabled)")
    
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1024,800")
    
    # Add additional stability options
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-plugins")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--allow-running-insecure-content")
    
    log.trace("Creating Chrome driver with options...")
    try:
        world.driver = webdriver.Chrome(options=chrome_options)
        world.driver.implicitly_wait(10)
        log.trace("Chrome driver initialized successfully for entire test session")
    except Exception as e:
        log.error(f"Failed to initialize Chrome driver: {e}")
        raise RuntimeError(f"ChromeDriver initialization failed: {e}") from e

@given("I go to home")
def i_go_to_home(step):
    """Navigate to the home page (base URL)."""
    _init_driver()
    base_url = world.base_url
    world.driver.get(base_url)
    
    # check the driver url after navigation (allow for redirects)
    assert base_url in world.driver.current_url
    
    # Wait for the page to load
    wait = WebDriverWait(world.driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "artifacts-container")))
    
    # Additional wait to ensure page is fully loaded and interactive
    time.sleep(3)

@step("I am on the main page")
def i_am_on_main_page(step):
    """Check that we are on the main page (expects previous step to have navigated)."""
    title = Title("iflow")
    title.locate(world.driver)

@when("I click the {button_text:QuotedString} button")
def i_click_button(step, button_text):
    """Click a button with the specified text."""
    button = Button(button_text)
    button.click(world.driver)

@then("the page title should be displayed")
def page_title_should_be_displayed(step):
    """Verify the page title is displayed."""
    title = Title("iflow")
    title.locate(world.driver)

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
