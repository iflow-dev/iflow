"""
Step definitions for iteration field functionality.
"""

from radish import given, when, then, step
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@then("I should see an iteration field")
def should_see_iteration_field(step):
    """Check that the iteration field is visible in the edit dialog."""
    from radish import world
    
    iteration_field = world.driver.find_element(By.ID, "artifactIteration")
    assert iteration_field.is_displayed(), "Iteration field should be visible"

@then("the field iteration is set to {value}")
def field_iteration_set_to(step, value):
    """Check that the iteration field has the specified value."""
    from radish import world
    
    iteration_field = world.driver.find_element(By.ID, "artifactIteration")
    actual_value = iteration_field.get_attribute("value")
    # Handle the case where value is quoted string
    expected_value = value.strip('"') if value.startswith('"') and value.endswith('"') else value
    assert actual_value == expected_value, f"Iteration field should be set to '{expected_value}', but got '{actual_value}'"

@step("I fill the iteration field with {text}")
def fill_iteration_field_with(step, text):
    """Fill the iteration field with the specified text."""
    from radish import world
    
    iteration_field = world.driver.find_element(By.ID, "artifactIteration")
    iteration_field.clear()
    iteration_field.send_keys(text)

@when("I fill in the iteration field with {text}")
def fill_iteration_field(step, text):
    """Fill in the iteration field with the specified text."""
    from radish import world
    
    iteration_field = world.driver.find_element(By.ID, "artifactIteration")
    iteration_field.clear()
    iteration_field.send_keys(text)

@when("I update the iteration field to {text}")
def update_iteration_field(step, text):
    """Update the iteration field with the specified text."""
    from radish import world
    
    iteration_field = world.driver.find_element(By.ID, "artifactIteration")
    iteration_field.clear()
    iteration_field.send_keys(text)

@given("there is an artifact with iteration {iteration}")
def artifact_with_iteration(step, iteration):
    """Ensure there is an artifact with the specified iteration."""
    # This step assumes the artifact already exists in the database
    # In a real test, you might want to create it programmatically
    pass

@given("there is an existing artifact")
def existing_artifact(step):
    """Ensure there is an existing artifact to edit."""
    # This step assumes the artifact already exists in the database
    # In a real test, you might want to create it programmatically
    pass

@then("the artifact should be saved with iteration {iteration}")
def artifact_saved_with_iteration(step, iteration):
    """Check that the artifact was saved with the specified iteration."""
    from radish import world
    
    # This step will need to be implemented based on how iteration is displayed
    # For now, we'll use "not implemented yet" as specified in the procedure
    step.context.not_implemented = True
    raise NotImplementedError("not implemented yet")

@then("I should see the iteration information displayed")
def should_see_iteration_displayed(step):
    """Check that iteration information is displayed in the artifact tile."""
    from radish import world
    
    # This step will need to be implemented based on how iteration is displayed
    # For now, we'll use "not implemented yet" as specified in the procedure
    step.context.not_implemented = True
    raise NotImplementedError("not implemented yet")

@then("it should show {iteration}")
def should_show_iteration(step, iteration):
    """Check that the displayed iteration matches the expected value."""
    from radish import world
    
    # This step will need to be implemented based on how iteration is displayed
    # For now, we'll use "not implemented yet" as specified in the procedure
    step.context.not_implemented = True
    raise NotImplementedError("not implemented yet")

@then("the artifact should be updated with new iteration {iteration}")
def artifact_updated_with_iteration(step, iteration):
    """Check that the artifact was updated with the new iteration."""
    from radish import world
    
    # This step will need to be implemented based on how iteration is displayed
    # For now, we'll use "not implemented yet" as specified in the procedure
    step.context.not_implemented = True
    raise NotImplementedError("not implemented yet")

@then("I see the iteration is set to {iteration}")
def see_iteration_set_to(step, iteration):
    """Check that the iteration is set to the specified value."""
    from radish import world
    
    # This step will need to be implemented based on how iteration is displayed
    # For now, we'll use "not implemented yet" as specified in the procedure
    step.context.not_implemented = True
    raise NotImplementedError("not implemented yet")

@step("I edit the first artifact")
def edit_first_artifact(step):
    """Edit the first artifact by clicking its edit button."""
    from radish import world
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    
    # Click the edit button on the first artifact
    edit_button = world.driver.find_element(By.XPATH, "//button[.//ion-icon[@name='create-outline']]")
    edit_button.click()
    
    # Wait for edit modal to appear
    wait = WebDriverWait(world.driver, 10)
    wait.until(EC.visibility_of_element_located((By.ID, "artifactDescription")))

@step("I click the edit button on the artifact")
def click_edit_button_on_artifact(step):
    """Click the edit button on an artifact."""
    from radish import world
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    
    # Click the edit button on an artifact
    edit_button = world.driver.find_element(By.XPATH, "//button[.//ion-icon[@name='create-outline']]")
    edit_button.click()
    
    # Wait for edit modal to appear
    wait = WebDriverWait(world.driver, 10)
    wait.until(EC.visibility_of_element_located((By.ID, "artifactDescription")))

@step("I click the Save button")
def click_save_button(step):
    """Click the Save button."""
    from radish import world
    from selenium.webdriver.common.by import By
    
    save_button = world.driver.find_element(By.XPATH, "//button[text()='Save']")
    save_button.click()

