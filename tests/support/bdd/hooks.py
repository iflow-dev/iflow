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
    

@after.all
def cleanup_test_environment(features, marker):
    """Clean up after all tests complete:

        - deinitialize ChromeDriver and close
    """
    log.trace("Starting BDD test environment cleanup...")
    
    log.trace("Closing Chrome driver...")
    world.driver.quit()
    log.trace("Chrome driver closed successfully")

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
    

@after.each_scenario
def after_scenario(scenario):
    """Clean up after each scenario."""
    log.trace(f"Cleaning up scenario: {scenario.sentence}")
    
    # Calculate scenario duration
    if hasattr(scenario, 'scenario_start_time'):
        duration = time.time() - scenario.scenario_start_time
        log.trace(f"Scenario completed in {duration:.2f} seconds")
    
    log.trace("Scenario cleanup completed")
    

# ============================================================================
# STEP-LEVEL HOOKS
# ============================================================================

@before.each_step
def before_step(step):
    """Check if dry-run mode is active and skip step execution if so."""
    print(f"DEBUG: HOOK EXECUTED for step: {step.sentence}")
    
    if world.config.dry_run:
        step.skip("DRY-RUN: SKIPPED")

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


log.error("HOOOOOOKS ARRREE LOAAAADED")
log.error("HOOOOOOKS ARRREE LOAAAADED")
