from radish import given, when, then, step
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up logging
log = logging.getLogger(__name__)

@step("I see artifacts displayed")
def i_see_artifacts_displayed(step):
    """Verify that artifacts are displayed on the page."""
    from radish import world
    
    # Wait for artifacts to be visible
    wait = WebDriverWait(world.driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "artifact-card")))
    log.debug("✅ Artifacts are displayed")

@when("I click the create button")
def i_click_create_button(step):
    """Click the create button to open the edit dialog for creating a new artifact."""
    from radish import world
    
    # Find and click the create button in the toolbar
    create_button = world.driver.find_element(By.XPATH, "//button[contains(text(), 'Create') and not(ancestor::div[contains(@class, 'modal')])]")
    create_button.click()
    log.debug("✅ Clicked create button")

@then("I should see the edit dialog")
def i_should_see_edit_dialog(step):
    """Verify that the edit dialog is visible."""
    from radish import world
    
    # Wait for the modal to be visible
    wait = WebDriverWait(world.driver, 10)
    modal = wait.until(EC.visibility_of_element_located((By.ID, "artifactModal")))
    
    # Verify the modal is displayed
    if modal.is_displayed():
        log.debug("✅ Edit dialog is visible")
    else:
        raise AssertionError("Edit dialog is not visible")

@then("the submit button should say {expected_text:QuotedString}")
def the_submit_button_should_say(step, expected_text):
    """Verify that the submit button has the expected text."""
    from radish import world
    
    # Find the submit button in the modal
    submit_button = world.driver.find_element(By.XPATH, "//div[@id='artifactModal']//button[@type='submit']")
    actual_text = submit_button.text.strip()
    
    if actual_text == expected_text:
        log.debug(f"✅ Submit button text is correct: '{actual_text}'")
    else:
        raise AssertionError(f"Submit button text should be '{expected_text}' but was '{actual_text}'")

@when("I click the edit button on the first artifact")
def i_click_edit_button_on_first_artifact(step):
    """Click the edit button on the first visible artifact."""
    from radish import world
    
    # Wait for artifacts to be visible
    wait = WebDriverWait(world.driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "artifact-card")))
    
    # Find and click the edit button on the first artifact (using ion-icon)
    edit_button = world.driver.find_element(By.XPATH, "//div[contains(@class, 'artifact-card')][1]//button[.//ion-icon[@name='create-outline']]")
    edit_button.click()
    log.debug("✅ Clicked edit button on first artifact")
