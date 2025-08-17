"""
World configuration for radish BDD tests.
This file sets up the test environment and provides shared state.
"""

from radish import world
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

from radish import before, after

@before.each_scenario
def before_scenario(scenario):
    """Set up the test environment before each scenario."""
    
    print("Setting up scenario...")
    
    # Set up Chrome options for visible testing (not headless)
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Commented out to show browser
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Initialize the web driver in world
    try:
        world.driver = webdriver.Chrome(options=chrome_options)
        world.driver.implicitly_wait(10)
        print("Chrome driver initialized successfully")
    except Exception as e:
        print(f"Warning: Could not initialize Chrome driver: {e}")
        print("Tests will run but may fail without a web driver")

@after.each_scenario
def after_scenario(scenario):
    """Clean up after each scenario."""
    
    print("Cleaning up scenario...")
    
    # Clean up the web driver from world
    if hasattr(world, 'driver') and world.driver:
        try:
            # Add a delay so you can see the result
            import time
            print("Waiting 5 seconds before closing browser...")
            time.sleep(5)
            
            world.driver.quit()
            print("Chrome driver closed successfully")
        except Exception as e:
            print(f"Error closing driver: {e}")
    else:
        print("No driver to clean up")

@before.all
def before_all(*args, **kwargs):
    """Set up before all tests run."""
    
    print("Starting BDD tests...")
    
    # Set base URL for the application
    import os
    base_url = os.getenv('IFLOW_BASE_URL', 'http://localhost:8081')
    print(f"Testing against: {base_url}")
    
    # Store in context if available
    if args and len(args) > 0:
        context = args[0]
        if hasattr(context, '__dict__'):
            context.base_url = base_url
            print(f"Base URL set in context: {context.base_url}")
        else:
            print("Context is not a proper object, cannot set base_url")
    else:
        print("No context available in before_all")

@after.all
def after_all(*args, **kwargs):
    """Clean up after all tests complete."""
    
    print("BDD testing completed")
