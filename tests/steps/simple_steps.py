"""
Simple step definitions for basic functionality testing.
"""

from radish import given, when, then
from selenium.webdriver.common.by import By
from controls import Title, Button
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@given("I go to home")
def i_go_to_home(step):
    """Navigate to the home page (base URL)."""
    from radish import world
    base_url = world.base_url
    world.driver.get(base_url)
    
    # check the driver url after navigation (allow for redirects)
    assert base_url in world.driver.current_url
    
    # Wait for the page to load
    wait = WebDriverWait(world.driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "artifacts-container")))

@given("I am on the main page")
def i_am_on_main_page(step):
    """Check that we are on the main page (expects previous step to have navigated)."""
    from radish import world
    title = Title("iflow")
    title.locate(world.driver)

@given("I am on the search page")
def i_am_on_search_page(step):
    """Check that we are on the search page (expects previous step to have navigated)."""
    from radish import world
    title = Title("iflow")
    title.locate(world.driver)

@when("I click the {button_text:QuotedString} button")
def i_click_button(step, button_text):
    """Click a button with the specified text."""
    from radish import world
    button = Button(button_text)
    button.click(world.driver)

@then("the page title should be displayed")
def page_title_should_be_displayed(step):
    """Verify the page title is displayed."""
    from radish import world
    title = Title("iflow")
    title.locate(world.driver)

@then("the artifact creation modal should be open")
def artifact_creation_modal_should_be_open(step):
    """Verify that the artifact creation modal is open."""
    from radish import world
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    # Wait for modal to be visible
    wait = WebDriverWait(world.driver, 10)
    modal = wait.until(
        EC.visibility_of_element_located((By.ID, "artifactModal"))
    )
    
    # Verify modal is displayed
    assert modal.is_displayed(), "Artifact creation modal is not displayed"
