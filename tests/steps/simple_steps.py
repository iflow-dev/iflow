"""
Simple step definitions for basic functionality testing.
"""

from radish import given, then
from selenium.webdriver.common.by import By
from controls import Title

@given("I go to home")
def i_go_to_home(step):
    """Navigate to the home page (base URL)."""
    from radish import world
    base_url = world.base_url
    world.driver.get(base_url)
    
    # check the driver url after navigation (allow for redirects)
    assert base_url in world.driver.current_url
    
    # Wait for the page to load
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    wait = WebDriverWait(world.driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "artifacts-container")))

@given("I am on the search page")
def i_am_on_search_page(step):
    """Check that we are on the search page (expects previous step to have navigated)."""
    from radish import world
    title = Title("iflow")
    title.locate(world.driver)

@then("the page title should be displayed")
def page_title_should_be_displayed(step):
    """Verify the page title is displayed."""
    from radish import world
    title = Title("iflow")
    title.locate(world.driver)
