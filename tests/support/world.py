"""
World configuration for radish BDD tests.
This file sets up the test environment and provides shared state.
"""

from radish import world
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import logging

from radish import before, after

# Set up logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

@before.all
def before_all(*args, **kwargs):
    """Set up before all tests run."""
    
    log.debug("Starting BDD tests...")
    
    # Set base URL for the application
    import os
    base_url = os.getenv('IFLOW_BASE_URL')
    if not base_url:
        raise ValueError("IFLOW_BASE_URL environment variable must be set")
    log.debug(f"Testing against: {base_url}")
    
    # Store base URL directly in world object for easy access
    world.base_url = base_url
    log.debug(f"Base URL set in world: {world.base_url}")
    
    # Initialize the web driver once for all tests
    log.debug("Initializing Chrome driver for all tests...")
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run headless by default
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    try:
        world.driver = webdriver.Chrome(options=chrome_options)
        world.driver.implicitly_wait(10)
        log.debug("Chrome driver initialized successfully")
    except Exception as e:
        log.debug(f"Warning: Could not initialize Chrome driver: {e}")
        log.debug("Tests will run but may fail without a web driver")

@after.all
def after_all(*args, **kwargs):
    """Clean up after all tests complete."""
    
    log.debug("BDD testing completed")
    
    # Clean up the web driver
    try:
        log.debug("Cleaning up BDD test environment...")
        world.driver.quit()
        log.debug("Chrome driver closed successfully")
    except Exception as e:
        log.debug(f"Error closing driver: {e}")

@before.each_scenario
def before_scenario(scenario):
    """Set up the test environment before each scenario."""
    
    log.debug(f"Setting up scenario: {scenario.sentence}")
    
    # Navigate to the base URL for each scenario to ensure clean state
    try:
        world.driver.get(world.base_url)
        log.debug(f"Navigated to: {world.base_url}")
    except Exception as e:
        log.debug(f"Warning: Could not navigate to base URL: {e}")

@after.each_scenario
def after_scenario(scenario):
    """Clean up after each scenario."""
    
    log.debug(f"Completed scenario: {scenario.sentence}")
    
    # Don't close the browser here - it will be closed in after_all
    # Just clear any scenario-specific state if needed
    pass
