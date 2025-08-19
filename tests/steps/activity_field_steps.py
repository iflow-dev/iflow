"""
Step definitions for activity field functionality.
"""

from radish import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@then("I should see an activity field")
def should_see_activity_field(step):
    """Check that the activity field is visible in the edit dialog."""
    from radish import world
    
    activity_field = world.driver.find_element(By.ID, "artifactActivity")
    assert activity_field.is_displayed(), "Activity field should be visible"

@then("the activity field should be empty by default")
def activity_field_empty_default(step):
    """Check that the activity field has no default value."""
    from radish import world
    
    activity_field = world.driver.find_element(By.ID, "artifactActivity")
    actual_value = activity_field.get_attribute("value")
    assert actual_value == "", f"Activity field should be empty by default, but got '{actual_value}'"

@then("I can edit the activity field")
def can_edit_activity_field(step):
    """Check that the activity field is editable."""
    from radish import world
    
    activity_field = world.driver.find_element(By.ID, "artifactActivity")
    assert activity_field.is_enabled(), "Activity field should be editable"

@when("I fill in the activity field with {text}")
def fill_activity_field(step, text):
    """Fill in the activity field with the specified text."""
    from radish import world
    
    activity_field = world.driver.find_element(By.ID, "artifactActivity")
    activity_field.clear()
    activity_field.send_keys(text)

@when("I update the activity field to {text}")
def update_activity_field(step, text):
    """Update the activity field with the specified text."""
    from radish import world
    
    activity_field = world.driver.find_element(By.ID, "artifactActivity")
    activity_field.clear()
    activity_field.send_keys(text)

@given("there is an artifact with activity {activity}")
def artifact_with_activity(step, activity):
    """Ensure there is an artifact with the specified activity."""
    # This step assumes the artifact already exists in the database
    # In a real test, you might want to create it programmatically
    pass

@given("there is an existing artifact")
def existing_artifact(step):
    """Ensure there is an existing artifact to edit."""
    # This step assumes the artifact already exists in the database
    # In a real test, you might want to create it programmatically
    pass

@then("the artifact should be saved with activity {activity}")
def artifact_saved_with_activity(step, activity):
    """Check that the artifact was saved with the specified activity."""
    from radish import world
    
    # This step will need to be implemented based on how activity is displayed
    # For now, we'll use "not implemented yet" as specified in the procedure
    step.context.not_implemented = True
    raise NotImplementedError("not implemented yet")

@then("I should see the activity information displayed")
def should_see_activity_displayed(step):
    """Check that activity information is displayed in the artifact tile."""
    from radish import world
    
    # This step will need to be implemented based on how activity is displayed
    # For now, we'll use "not implemented yet" as specified in the procedure
    step.context.not_implemented = True
    raise NotImplementedError("not implemented yet")

@then("it should show {activity}")
def should_show_activity(step, activity):
    """Check that the displayed activity matches the expected value."""
    from radish import world
    
    # This step will need to be implemented based on how activity is displayed
    # For now, we'll use "not implemented yet" as specified in the procedure
    step.context.not_implemented = True
    raise NotImplementedError("not implemented yet")

@then("the artifact should be updated with new activity {activity}")
def artifact_updated_with_activity(step, activity):
    """Check that the artifact was updated with the new activity."""
    from radish import world
    
    # This step will need to be implemented based on how activity is displayed
    # For now, we'll use "not implemented yet" as specified in the procedure
    step.context.not_implemented = True
    raise NotImplementedError("not implemented yet")
