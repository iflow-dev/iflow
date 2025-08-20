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

@when("I set activity to {text}")
def set_activity_to(step, text):
    """Set the activity field to the specified text."""
    from radish import world
    
    activity_field = world.driver.find_element(By.ID, "artifactActivity")
    activity_field.clear()
    activity_field.send_keys(text)



@then("the artifact should be saved with activity {activity}")
def artifact_saved_with_activity(step, activity):
    """Check that the artifact was saved with the specified activity."""
    from radish import world
    
    # Check that the activity field contains the expected value
    activity_field = world.driver.find_element(By.ID, "artifactActivity")
    actual_value = activity_field.get_attribute("value")
    assert actual_value == activity, f"Activity should be '{activity}', but got '{actual_value}'"

@then("I should see the activity information displayed")
def should_see_activity_displayed(step):
    """Check that activity information is displayed in the artifact tile."""
    from radish import world
    
    # Check that the activity field is visible and contains text
    activity_field = world.driver.find_element(By.ID, "artifactActivity")
    assert activity_field.is_displayed(), "Activity field should be visible"
    actual_value = activity_field.get_attribute("value")
    assert actual_value, "Activity field should contain text"

@then("it should show {activity}")
def should_show_activity(step, activity):
    """Check that the displayed activity matches the expected value."""
    from radish import world
    
    # Check that the activity field shows the expected value
    activity_field = world.driver.find_element(By.ID, "artifactActivity")
    actual_value = activity_field.get_attribute("value")
    assert actual_value == activity, f"Activity should show '{activity}', but got '{actual_value}'"

@then("the artifact should be updated with new activity {activity}")
def artifact_updated_with_activity(step, activity):
    """Check that the artifact was updated with the new activity."""
    from radish import world
    
    # Check that the activity field contains the updated value
    activity_field = world.driver.find_element(By.ID, "artifactActivity")
    actual_value = activity_field.get_attribute("value")
    assert actual_value == activity, f"Activity should be updated to '{activity}', but got '{actual_value}'"
