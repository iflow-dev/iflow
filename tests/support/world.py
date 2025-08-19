"""
World configuration for radish BDD tests.
This file sets up the test environment and provides shared state.
"""

from radish import world
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

from radish import before, after

@before.all
def before_all(*args, **kwargs):
    """Set up before all tests run."""
    
    print("Starting BDD tests...")
    
    # Set base URL for the application
    import os
    base_url = os.getenv('IFLOW_BASE_URL')
    if not base_url:
        raise ValueError("IFLOW_BASE_URL environment variable must be set")
    print(f"Testing against: {base_url}")
    
    # Store base URL directly in world object for easy access
    world.base_url = base_url
    print(f"Base URL set in world: {world.base_url}")
    
    # Set up Chrome options for headless testing
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run headless by default
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Initialize the web driver once for the entire test session
    try:
        world.driver = webdriver.Chrome(options=chrome_options)
        world.driver.implicitly_wait(10)
        print("Chrome driver initialized successfully for entire test session")
    except Exception as e:
        print(f"Warning: Could not initialize Chrome driver: {e}")
        print("Tests will run but may fail without a web driver")

@after.all
def after_all(*args, **kwargs):
    """Clean up after all tests complete."""
    
    print("BDD testing completed")
    
    # Clean up the web driver from world
    if hasattr(world, 'driver') and world.driver:
        try:
            print("Closing Chrome driver...")
            world.driver.quit()
            print("Chrome driver closed successfully")
        except Exception as e:
            print(f"Error closing driver: {e}")
    else:
        print("No driver to clean up")

@before.each_scenario
def before_scenario(scenario):
    """Set up the test environment before each scenario."""
    
    print("Setting up scenario...")
    
    # Initialize scenario-specific state
    import time
    scenario.scenario_start_time = time.time()
    scenario.current_page = None
    scenario.last_action = None

@after.each_scenario
def after_scenario(scenario):
    """Clean up after each scenario."""
    
    # Calculate scenario duration
    import time
    scenario_duration = time.time() - scenario.scenario_start_time
    print(f"Completed scenario: {scenario.sentence} in {scenario_duration:.2f}s")
    
    # Clean up scenario state
    scenario.current_page = None
    scenario.last_action = None
    
    # Note: ChromeDriver is NOT closed here - it stays alive for the entire session
