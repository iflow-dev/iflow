"""
Step definitions for activity field functionality.
"""

from radish import given, when, then, step
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@then("I should see an activity field")
def should_see_activity_field(step):
    """Check that the activity field is visible in the edit dialog."""
    from radish import world
    
    activity_field = world.driver.find_element(By.ID, "artifactActivity")
    assert activity_field.is_displayed(), "Activity field should be visible"

@then("the activity field is empty")
def activity_field_is_empty(step):
    """Check that the activity field has no default value."""
    from radish import world
    
    activity_field = world.driver.find_element(By.ID, "artifactActivity")
    actual_value = activity_field.get_attribute("value")
    assert actual_value == "", f"Activity field should be empty, but got '{actual_value}'"

@when("I set activity to {text}")
def set_activity_to(step, text):
    """Set the activity field to the specified text."""
    from radish import world
    
    activity_field = world.driver.find_element(By.ID, "artifactActivity")
    activity_field.clear()
    activity_field.send_keys(text)

# TODO: replace usage by "I open the artifact <summary>"
@step("I open the artifact with title \"{title}\"")
def open_artifact_with_title(step, title):
    """Open an artifact with the specified title for editing."""
    from radish import world
    
    # Find the artifact with the specified title and click its edit button
    artifacts = world.driver.find_elements(By.CLASS_NAME, "artifact-card")
    
    for artifact in artifacts:
        try:
            summary_element = artifact.find_element(By.CLASS_NAME, "artifact-summary")
            if summary_element.text == title:
                edit_button = artifact.find_element(By.CSS_SELECTOR, "button[onclick*='openEditModal']")
                edit_button.click()
                return
        except Exception as e:
            continue
    
    raise AssertionError(f"Artifact with title '{title}' not found")

@then("I see the activity is {activity}")
def see_activity_is(step, activity):
    """Check that the activity field shows the specified value."""
    from radish import world
    
    # Check that the activity field contains the expected value
    activity_field = world.driver.find_element(By.ID, "artifactActivity")
    actual_value = activity_field.get_attribute("value")
    assert actual_value == activity, f"Activity should be '{activity}', but got '{actual_value}'"


