from radish import before, after, world
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import time
from bdd.logging import logger

@before.all
def setup_test_environment(features, marker):
    """Set up the test environment before all tests."""
    logger.trace("Starting BDD test environment setup...")
    
    # Initialize world.driver to None
    world.driver = None
    logger.trace("world.driver initialized to None")


# Global driver variable accessible to @after.all hook
global_driver = None

def _preinit():
    # Set base URL for the application
    base_url = os.getenv('IFLOW_BASE_URL')
    if not base_url:
        logger.trace("IFLOW_BASE_URL environment variable not set")
        raise ValueError("IFLOW_BASE_URL environment variable must be set")
    logger.trace(f"Testing against: {base_url}")

    # Store base URL directly in world object for easy access
    world.base_url = base_url
    logger.trace(f"Base URL set in world: {world.base_url}")


def _init_driver():
    global global_driver
    
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
    
    # Store reference for @after.all cleanup
    global_driver = world.driver
    logger.trace("Driver created and stored globally for cleanup")


@after.all
def cleanup_test_environment(features, marker):
    """Clean up the driver at the end of all tests."""
    global global_driver
    if global_driver is not None:
        logger.trace("Cleaning up driver in @after.all")
        global_driver.quit()
        global_driver = None
        logger.trace("Driver cleanup completed")
    else:
        logger.trace("No driver to cleanup (dry-run mode or no driver created)")


@before.each_scenario
def before_scenario(scenario):
    """Set up the test environment before each scenario."""
    logger.trace(f"Setting up scenario: {scenario.sentence}")
    
    # Skip driver creation in dry-run mode
    if hasattr(world, 'config') and hasattr(world.config, 'dry_run') and world.config.dry_run:
        logger.trace("Dry-run mode: Skipping driver creation")
        world.driver = None
    # Create driver only on first scenario (non-dry-run mode)
    elif world.driver is None:
        logger.trace("Creating driver for first scenario")
        _init_driver()
    else:
        logger.trace("Reusing existing driver for scenario")

    # Initialize scenario-specific state
    scenario.scenario_start_time = time.time()
    scenario.current_page = None
    scenario.last_action = None
    logger.trace("Scenario state initialized")


@after.each_scenario
def after_scenario(scenario):
    """Clean up after each scenario."""
    logger.trace(f"Cleaning up scenario: {scenario.sentence}")

    # Calculate scenario duration
    if hasattr(scenario, 'scenario_start_time'):
        duration = time.time() - scenario.scenario_start_time
        logger.trace(f"Scenario completed in {duration:.2f} seconds")

    logger.trace("Scenario cleanup completed")


@before.each_step
def before_step(step):
    # Add a delay of 2 seconds before each step when in foreground mode
    headless_mode = os.environ.get("HEADLESS_MODE", "true").lower() == "true"
    if not headless_mode:
        time.sleep(2)


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
        logger.debug(f"Screenshot saved: {filename}")
    except Exception as e:
        logger.debug(f"Could not take screenshot: {e}")

def log_test_step(context, step_name, details=None):
    """Log test step execution for debugging."""
    timestamp = time.strftime("%H:%M:%S")
    log_entry = f"[{timestamp}] {step_name}"
    if details:
        log_entry += f" - {details}"
    logger.debug(log_entry)
    context.last_action = step_name


logger.error("HOOOOOOKS ARRREE LOAAAADED")
logger.error("HOOOOOOKS ARRREE LOAAAADED")
