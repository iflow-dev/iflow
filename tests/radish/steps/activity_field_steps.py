"""
Step definitions for activity field functionality.
"""

from radish import when, then, step, world
from selenium.webdriver.common.by import By


@then("I should see an activity field")
def should_see_activity_field(step):
    activity_field = world.driver.find_element(By.ID, "artifactActivity")
    assert activity_field.is_displayed(), "Activity field should be visible"


@then("the activity field is empty")
def activity_field_is_empty(step):
    activity_field = world.driver.find_element(By.ID, "artifactActivity")
    actual_value = activity_field.get_attribute("value")
    assert actual_value == "", (
        f"Activity field should be empty, but got '{actual_value}'"
    )


@when("I set activity to {text}")
def set_activity_to(step, text):
    activity_field = world.driver.find_element(By.ID, "artifactActivity")
    activity_field.clear()
    activity_field.send_keys(text)


# TODO: replace usage by "I open the artifact <summary>"
@step("I open the artifact with title \"{title}\"")
def open_artifact_with_title(step, title):
    artifacts = world.driver.find_elements(By.CLASS_NAME, "artifact-card")

    for artifact in artifacts:
        try:
            summary_element = artifact.find_element(
                By.CLASS_NAME, "artifact-summary"
            )
            if summary_element.text == title:
                edit_button = artifact.find_element(
                    By.CSS_SELECTOR, "button[onclick*='openEditModal']"
                )
                edit_button.click()
                return
        except Exception:
            continue

    raise AssertionError(f"Artifact with title '{title}' not found")


@then("I see the activity is {activity}")
def see_activity_is(step, activity):
    activity_field = world.driver.find_element(By.ID, "artifactActivity")
    actual_value = activity_field.get_attribute("value")
    assert actual_value == activity, (
        f"Activity should be '{activity}', but got '{actual_value}'"
    )
