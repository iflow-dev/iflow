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
    

# TODO:
#
# When activated, it looks like this hook is running
# BETWEEN the scenarios instead of after them.
# This causes the driver to deinitialize after the first
# scenario.
# 
# @after.all
def cleanup_test_environment(features, marker):
    """Clean up after all tests complete:

        - deinitialize ChromeDriver and close
    """
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
# STEP-LEVEL HOOKS
# ============================================================================

@before.each_step
def before_step(step):
    """Check if dry-run mode is active and skip step execution if so."""
    print(f"DEBUG: HOOK EXECUTED for step: {step.sentence}")
    
    try:
        # Debug: Check what's available in world
        print(f"DEBUG: world attributes: {dir(world)}")
        if hasattr(world, 'config'):
            print(f"DEBUG: world.config attributes: {dir(world.config)}")
            if hasattr(world.config, 'dry_run'):
                print(f"DEBUG: world.config.dry_run = {world.config.dry_run}")
            else:
                print(f"DEBUG: world.config.dry_run not found")
        else:
            print(f"DEBUG: world.config not found")
        
        # Check if dry-run mode is enabled in world.config
        if hasattr(world, 'config') and hasattr(world.config, 'dry_run') and world.config.dry_run:
            log.trace(f"DRY-RUN MODE: Skipping step execution for: {step.sentence}")
            step.skip("Dry-run mode: skipping step execution")
            return
        else:
            print(f"DEBUG: Dry-run mode not enabled, continuing with step: {step.sentence}")
    except Exception as e:
        # If we can't check dry-run mode, continue with normal execution
        log.trace(f"Could not check dry-run mode, continuing with step: {e}")
        print(f"DEBUG: Exception checking dry-run mode: {e}")
        pass
    
    # Normal step execution continues
    log.trace(f"Executing step: {step.sentence}")

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
