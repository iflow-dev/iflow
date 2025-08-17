"""
Hooks for radish BDD tests.
This file contains test lifecycle hooks and utilities.
"""

from radish import before, after, before_all, after_all
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

@before.all
def setup_test_environment(features, context):
    """Set up the test environment before all tests."""
    print("Setting up BDD test environment...")
    
    # Set default timeout for waits
    context.default_timeout = 10
    
    # Set up test configuration
    context.test_config = {
        'headless': True,
        'window_size': (1920, 1080),
        'implicit_wait': 10
    }

@after.all
def cleanup_test_environment(features, context):
    """Clean up after all tests complete."""
    print("Cleaning up BDD test environment...")
    
    # Any final cleanup can go here
    pass

@before.each_scenario
def setup_scenario(scenario, context):
    """Set up before each scenario."""
    print(f"Starting scenario: {scenario.name}")
    
    # Initialize scenario-specific state
    context.scenario_start_time = time.time()
    context.current_page = None
    context.last_action = None

@after.each_scenario
def cleanup_scenario(scenario, context):
    """Clean up after each scenario."""
    scenario_duration = time.time() - context.scenario_start_time
    print(f"Completed scenario: {scenario.name} in {scenario_duration:.2f}s")
    
    # Clean up scenario state
    context.current_page = None
    context.last_action = None

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
        print(f"Screenshot saved: {filename}")
    except Exception as e:
        print(f"Could not take screenshot: {e}")

def log_test_step(context, step_name, details=None):
    """Log test step execution for debugging."""
    timestamp = time.strftime("%H:%M:%S")
    log_entry = f"[{timestamp}] {step_name}"
    if details:
        log_entry += f" - {details}"
    print(log_entry)
    context.last_action = step_name
