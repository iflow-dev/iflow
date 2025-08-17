"""
World configuration for radish BDD tests.
This file sets up the test environment and provides shared state.
"""

from radish import world
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

def before_scenario(scenario, context):
    """Set up the test environment before each scenario."""
    
    # Set up Chrome options for headless testing
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Initialize the web driver
    try:
        context.driver = webdriver.Chrome(options=chrome_options)
        context.driver.implicitly_wait(10)
    except Exception as e:
        print(f"Warning: Could not initialize Chrome driver: {e}")
        print("Tests will run but may fail without a web driver")
        context.driver = None
    
    # Initialize test state
    context.current_artifact_id = None
    context.filter_state = {}
    context.wait = None

def after_scenario(scenario, context):
    """Clean up after each scenario."""
    
    # Close the web driver
    if hasattr(context, 'driver') and context.driver:
        try:
            context.driver.quit()
        except:
            pass
    
    # Clear test state
    context.current_artifact_id = None
    context.filter_state = {}
    context.wait = None

def before_all(features, context):
    """Set up before all tests run."""
    
    # Set base URL for the application
    context.base_url = os.getenv('IFLOW_BASE_URL', 'http://localhost:8080')
    
    # Set up test data
    context.test_data = {
        'sample_artifact': {
            'type': 'requirement',
            'summary': 'Test requirement for BDD testing',
            'description': 'This is a test requirement created during BDD testing',
            'category': 'Testing',
            'status': 'open'
        }
    }
    
    print(f"Starting BDD tests against: {context.base_url}")

def after_all(features, context):
    """Clean up after all tests complete."""
    
    print("BDD testing completed")
    
    # Clean up any test artifacts if needed
    if hasattr(context, 'driver') and context.driver:
        try:
            context.driver.quit()
        except:
            pass
