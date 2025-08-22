"""
Hooks for radish BDD tests.
This file contains test lifecycle hooks and utilities.
"""

from radish import before, after, world
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import time
from bdd.logging_config import logger as log

@before.all
def setup_test_environment(features, marker):
    """Set up the test environment before all tests."""
    log.trace("Starting BDD test environment setup...")


driver = None

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
    _preinit()

    chrome_options = Options()

    headless_mode = os.environ.get("HEADLESS_MODE", "true").lower() == "true"
    if headless_mode:
        chrome_options.add_argument("--headless")

    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1024,800")

    # Add additional stability options
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-plugins")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--allow-running-insecure-content")

    world.driver = webdriver.Chrome(options=chrome_options)
    world.driver.implicitly_wait(1)
    driver = world.driver


@after.all
def cleanup_test_environment(features, marker):
    if driver is not None:
        driver.quit()


@before.each_scenario
def before_scenario(scenario):
    """Set up the test environment before each scenario."""
    log.trace(f"Setting up scenario: {scenario.sentence}")
    if driver is None:
        _init_driver()

    # Initialize scenario-specific state
    scenario.scenario_start_time = time.time()
    scenario.current_page = None
    scenario.last_action = None
    log.trace("Scenario state initialized")


@after.each_scenario
def after_scenario(scenario):
    """Clean up after each scenario."""
    log.trace(f"Cleaning up scenario: {scenario.sentence}")

    # Calculate scenario duration
    if hasattr(scenario, 'scenario_start_time'):
        duration = time.time() - scenario.scenario_start_time
        log.trace(f"Scenario completed in {duration:.2f} seconds")

    log.trace("Scenario cleanup completed")


@before.each_step
def before_step(step):
    pass


def wait_for_element(driver, by, value, timeout=10):
    """Wait for an element to be present and visible."""
    wait = WebDriverWait(driver, timeout)
    return wait.until(EC.visibility_of_element_located((by, value)))

def wait_for_element_clickable(driver, by, value, timeout=10):
    """Wait for an element to be clickable."""
    wait = WebDriverWait(driver, timeout)
    return wait.until(EC.element_to_be_clickable((by, value)))

def take_screenshot(driver, name):
    """Take a screenshot for debugging purposes."""
    try:
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"test_screenshots/{name}_{timestamp}.png"
        driver.save_screenshot(filename)
        log.debug(f"Screenshot saved: {filename}")
    except Exception as e:
        log.debug(f"Could not take screenshot: {e}")

def log_test_step(context, step_name, details=None):
    """Log test step execution for debugging."""
    timestamp = time.strftime("%H:%M:%S")
    log_entry = f"[{timestamp}] {step_name}"
    if details:
        log_entry += f" - {details}"
    log.debug(log_entry)
    context.last_action = step_name


log.error("HOOOOOOKS ARRREE LOAAAADED")
log.error("HOOOOOOKS ARRREE LOAAAADED")
