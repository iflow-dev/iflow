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
from logging_config import logger as log

# ============================================================================
# SESSION-LEVEL HOOKS (ChromeDriver Management)
# ============================================================================

@before.all
def setup_test_environment(features, marker):
    """Set up the test environment before all tests."""
    log.trace("Starting BDD test environment setup...")
    
    # Set base URL for the application
    base_url = os.getenv('IFLOW_BASE_URL')
    if not base_url:
        log.trace("IFLOW_BASE_URL environment variable not set")
        raise ValueError("IFLOW_BASE_URL environment variable must be set")
    log.trace(f"Testing against: {base_url}")
    
    # Store base URL directly in world object for easy access
    world.base_url = base_url
    log.trace(f"Base URL set in world: {world.base_url}")
    
    # Initialize the web driver once for the entire test session
    log.trace("Initializing Chrome driver for entire test session...")
    chrome_options = Options()
    
    # Check if headless mode should be disabled
    headless_mode = os.environ.get("HEADLESS_MODE", "true").lower() == "true"
    if headless_mode:
        chrome_options.add_argument("--headless")  # Run headless by default
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
    
    try:
        log.trace("Creating Chrome driver with options...")
        world.driver = webdriver.Chrome(options=chrome_options)
        world.driver.implicitly_wait(10)
        log.trace("Chrome driver initialized successfully for entire test session")
    except Exception as e:
        log.error(f"Failed to initialize Chrome driver: {e}")
        raise RuntimeError(f"ChromeDriver initialization failed: {e}") from e

# @after.all
def cleanup_test_environment(features, marker):
    """Clean up after all tests complete."""
    log.trace("Starting BDD test environment cleanup...")
    
    # Clean up the web driver from world
    if hasattr(world, 'driver') and world.driver:
        try:
            log.trace("Closing Chrome driver...")
            world.driver.quit()
            log.trace("Chrome driver closed successfully")
        except Exception as e:
            log.trace(f"Error closing driver: {e}")
    else:
        log.trace("No driver to clean up")
    
    log.trace("BDD test environment cleanup completed")

# ============================================================================
# SCENARIO-LEVEL HOOKS
# ============================================================================

@before.each_scenario
def before_scenario(scenario):
    """Set up the test environment before each scenario."""
    log.trace(f"Setting up scenario: {scenario.sentence}")
    
    # Initialize scenario-specific state
    scenario.scenario_start_time = time.time()
    scenario.current_page = None
    scenario.last_action = None
    log.trace("Scenario state initialized")
    
    # Navigate to the base URL for each scenario to ensure clean state
    try:
        log.trace(f"Navigating to base URL: {world.base_url}")
        world.driver.get(world.base_url)
        log.trace(f"Successfully navigated to: {world.base_url}")
    except Exception as e:
        log.trace(f"Warning: Could not navigate to base URL: {e}")

@after.each_scenario
def after_scenario(scenario):
    """Clean up after each scenario."""
    log.trace(f"Cleaning up scenario: {scenario.sentence}")
    
    # Calculate scenario duration
    if hasattr(scenario, 'scenario_start_time'):
        duration = time.time() - scenario.scenario_start_time
        log.trace(f"Scenario completed in {duration:.2f} seconds")
    
    log.trace("Scenario cleanup completed")
    
    # Close any open modal to ensure clean state for next scenario
    try:
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        # Check if modal is open
        modal = world.driver.find_element(By.ID, "artifactModal")
        if modal.is_displayed():
            log.debug("Closing open modal after scenario")
            # Try to find and click the close button (×)
            close_button = world.driver.find_element(By.XPATH, "//div[@id='artifactModal']//button[contains(text(), '×') or contains(@class, 'close')]")
            close_button.click()
            # Wait for modal to close
            WebDriverWait(world.driver, 5).until(EC.invisibility_of_element_located((By.ID, "artifactModal")))
            log.debug("Modal closed successfully")
    except Exception as e:
        log.debug(f"No modal to close or error closing modal: {e}")
    
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
