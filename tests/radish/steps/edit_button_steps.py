from radish import when, then, world
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bdd.logging_config import logger

# Note: "I see artifacts displayed" step is already defined in
# artifact_flags_steps.py


@when("I click the create button")
def i_click_create_button(step):
    # Find and click the create button in the toolbar
    create_button = world.driver.find_element(
        By.XPATH,
        "//button[contains(text(), 'Create') and "
        "not(ancestor::div[contains(@class, 'modal')])]"
    )
    create_button.click()
    logger.debug("✅ Clicked create button")


@then("I should see the edit dialog")
def i_should_see_edit_dialog(step):
    # Wait for the modal to be visible
    wait = WebDriverWait(world.driver, 10)
    modal = wait.until(
        EC.visibility_of_element_located((By.ID, "artifactModal"))
    )

    # Verify the modal is displayed
    if modal.is_displayed():
        logger.debug("✅ Edit dialog is visible")
    else:
        raise AssertionError("Edit dialog is not visible")


@then("the submit button should say {expected_text:QuotedString}")
def the_submit_button_should_say(step, expected_text):
    # Find the submit button in the modal
    submit_button = world.driver.find_element(
        By.XPATH,
        "//div[@id='artifactModal']//button[@type='submit']"
    )
    actual_text = submit_button.text.strip()

    if actual_text == expected_text:
        logger.debug(f"✅ Submit button text is correct: '{actual_text}'")
    else:
        raise AssertionError(
            f"Submit button text should be '{expected_text}' "
            f"but was '{actual_text}'"
        )


@when("I click the edit button on the first artifact")
def i_click_edit_button_on_first_artifact(step):
    # Wait for artifacts to be visible
    wait = WebDriverWait(world.driver, 10)
    wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "artifact-tile"))
    )

    # Find and click the edit button on the first artifact
    edit_button = world.driver.find_element(
        By.XPATH,
        "//div[contains(@class, 'artifact-tile')][1]//"
        "button[.//ion-icon[@name='create-outline']]"
    )
    edit_button.click()
    logger.debug("✅ Clicked edit button on first artifact")
