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
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

# ============================================================================
# SESSION-LEVEL HOOKS (ChromeDriver Management)
# ============================================================================

@before.all
def setup_test_environment(features, marker):
    """Set up the test environment before all tests."""
    log.debug("Starting BDD tests...")
    
    # Set base URL for the application
    base_url = os.getenv('IFLOW_BASE_URL')
    if not base_url:
        raise ValueError("IFLOW_BASE_URL environment variable must be set")
    log.debug(f"Testing against: {base_url}")
    
    # Store base URL directly in world object for easy access
    world.base_url = base_url
    log.debug(f"Base URL set in world: {world.base_url}")
    
    # Initialize the web driver once for the entire test session
    log.debug("Initializing Chrome driver for entire test session...")
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run headless by default
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    try:
        world.driver = webdriver.Chrome(options=chrome_options)
        world.driver.implicitly_wait(10)
        log.debug("Chrome driver initialized successfully for entire test session")
    except Exception as e:
        log.debug(f"Warning: Could not initialize Chrome driver: {e}")
        log.debug("Tests will run but may fail without a web driver")

# @after.all
def cleanup_test_environment(features, marker):
    """Clean up after all tests complete."""
    log.debug("BDD testing completed")
    
    # Clean up the web driver from world
    if hasattr(world, 'driver') and world.driver:
        try:
            log.debug("Closing Chrome driver...")
            world.driver.quit()
            log.debug("Chrome driver closed successfully")
        except Exception as e:
            log.debug(f"Error closing driver: {e}")
    else:
        log.debug("No driver to clean up")

# ============================================================================
# SCENARIO-LEVEL HOOKS
# ============================================================================

@before.each_scenario
def before_scenario(scenario):
    """Set up the test environment before each scenario."""
    log.debug(f"Setting up scenario: {scenario.sentence}")
    
    # Initialize scenario-specific state
    scenario.scenario_start_time = time.time()
    scenario.current_page = None
    scenario.last_action = None
    
    # Navigate to the base URL for each scenario to ensure clean state
    try:
        world.driver.get(world.base_url)
        log.debug(f"Navigated to: {world.base_url}")
    except Exception as e:
        log.debug(f"Warning: Could not navigate to base URL: {e}")

@after.each_scenario
def after_scenario(scenario):
    """Clean up after each scenario."""
    # Calculate scenario duration
    scenario_duration = time.time() - scenario.scenario_start_time
    log.debug(f"Completed scenario: {scenario.sentence} in {scenario_duration:.2f}s")
    
    # Clean up scenario state
    scenario.current_page = None
    scenario.last_action = None
    
    # Note: ChromeDriver is NOT closed here - it stays alive for the entire session

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

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
