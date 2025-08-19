"""
Step definitions for iteration field functionality.
"""

from radish import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@then("I should see an iteration field")
def should_see_iteration_field(step):
    """Check that the iteration field is visible in the edit dialog."""
    from radish import world
    
    iteration_field = world.driver.find_element(By.ID, "artifactIteration")
    assert iteration_field.is_displayed(), "Iteration field should be visible"

@then("the iteration field should be empty by default")
def iteration_field_empty_default(step):
    """Check that the iteration field has no default value."""
    from radish import world
    
    iteration_field = world.driver.find_element(By.ID, "artifactIteration")
    actual_value = iteration_field.get_attribute("value")
    assert actual_value == "", f"Iteration field should be empty by default, but got '{actual_value}'"

@then("I can edit the iteration field")
def can_edit_iteration_field(step):
    """Check that the iteration field is editable."""
    from radish import world
    
    iteration_field = world.driver.find_element(By.ID, "artifactIteration")
    assert iteration_field.is_enabled(), "Iteration field should be editable"

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
