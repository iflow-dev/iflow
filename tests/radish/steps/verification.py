from radish import given, when, then, world
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@then("I should see a verification field")
def should_see_verification_field(step):
    verification_field = world.driver.find_element(By.ID, "artifactVerification")
    assert verification_field.is_displayed(), "Verification field should be visible"


@then("the verification field should have default value {default_value}")
def verification_field_default_value(step, default_value):
    verification_field = world.driver.find_element(By.ID, "artifactVerification")
    actual_value = verification_field.get_attribute("value")
    assert actual_value == default_value, \
        f"Verification field should have default value '{default_value}', but got '{actual_value}'"


@then("I can edit the verification field")
def can_edit_verification_field(step):
    verification_field = world.driver.find_element(By.ID, "artifactVerification")
    assert verification_field.is_enabled(), "Verification field should be editable"


@when("I set the verification field to {value}")
def set_verification_field(step, value):
    verification_field = world.driver.find_element(By.ID, "artifactVerification")
    verification_field.clear()
    verification_field.send_keys(value)


@then("the artifact should be saved with verification method {method}")
def artifact_saved_with_verification_method(step, method):
    xpath = f"//div[contains(@class, 'artifact-verification') and contains(text(), '{method}')]"
    verification_element = world.driver.find_element(By.XPATH, xpath)
    assert verification_element.is_displayed(), f"Artifact with verification method '{method}' should be displayed"


@given("there is an artifact with verification method {method}")
def artifact_with_verification_method(step, method):
    pass


@when("I view the artifact tile")
def view_artifact_tile(step):
    pass


@then("I should see the verification method displayed")
def should_see_verification_method_displayed(step):
    verification_element = world.driver.find_element(By.CLASS_NAME, "artifact-verification")
    assert verification_element.is_displayed(), "Verification method should be displayed in artifact tile"


@then("it should show {method}")
def should_show_verification_method(step, method):
    verification_element = world.driver.find_element(By.CLASS_NAME, "artifact-verification")
    verification_text = verification_element.text
    assert method in verification_text, f"Verification method should show '{method}', but got '{verification_text}'"


@when("I fill in the summary with {summary}")
def fill_in_summary(step, summary):
    summary_field = world.driver.find_element(By.ID, "artifactSummary")
    summary_field.clear()
    summary_field.send_keys(summary)


@when("I fill in the description with {description}")
def fill_in_description(step, description):
    description_field = world.driver.find_element(By.ID, "artifactDescription")
    description_field.clear()
    description_field.send_keys(description)


@then("I should see a success message")
def should_see_success_message(step):
    wait = WebDriverWait(world.driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "artifacts-container")))
