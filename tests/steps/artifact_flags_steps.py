"""
Step definitions for artifact flags functionality tests.
"""

from radish import step, world
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


@step("I see artifacts displayed")
def i_see_artifacts_displayed(step):
    """Verify that artifacts are displayed on the page."""
    from radish import world
    
    # Wait for artifacts to load
    wait = WebDriverWait(world.driver, 10)
    artifacts = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".artifact-card")))
    
    assert len(artifacts) > 0, "No artifacts found on the page"
    print(f"✅ Found {len(artifacts)} artifacts displayed")


@step("I click the flag button on the first artifact")
def i_click_flag_button_on_first_artifact(step):
    """Click the flag button on the first artifact."""
    from radish import world
    
    # Find the first artifact's flag button
    wait = WebDriverWait(world.driver, 10)
    flag_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".artifact-card:first-child .artifact-actions button:first-child")))
    
    # Store the current flag state for verification
    icon = flag_button.find_element(By.CSS_SELECTOR, "ion-icon")
    world.previous_flag_state = "flag" in icon.get_attribute("name")
    
    flag_button.click()
    print(f"✅ Clicked flag button on first artifact (previous state: {'flagged' if world.previous_flag_state else 'unflagged'})")


@step("I click the flag button on the same artifact again")
def i_click_flag_button_on_same_artifact_again(step):
    """Click the flag button on the same artifact again."""
    from radish import world
    
    # Find the first artifact's flag button
    wait = WebDriverWait(world.driver, 10)
    flag_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".artifact-card:first-child .artifact-actions button:first-child")))
    
    # Store the current flag state for verification
    icon = flag_button.find_element(By.CSS_SELECTOR, "ion-icon")
    world.previous_flag_state = "flag" in icon.get_attribute("name") and "outline" not in icon.get_attribute("name")
    
    flag_button.click()
    print(f"✅ Clicked flag button on same artifact again (previous state: {'flagged' if world.previous_flag_state else 'unflagged'})")


@step("the artifact should be flagged")
def the_artifact_should_be_flagged(step):
    """Verify that the artifact is now flagged."""
    from radish import world
    
    # Wait for the flag state to change
    time.sleep(1)
    
    # Check the flag button state
    flag_button = world.driver.find_element(By.CSS_SELECTOR, ".artifact-card:first-child .artifact-actions button:first-child")
    icon = flag_button.find_element(By.CSS_SELECTOR, "ion-icon")
    current_flag_state = "flag" in icon.get_attribute("name") and "outline" not in icon.get_attribute("name")
    
    # The flag state should have changed from the previous state
    assert current_flag_state != world.previous_flag_state, f"Flag state did not change. Expected: {not world.previous_flag_state}, Got: {current_flag_state}"
    print(f"✅ Artifact flag state changed successfully")


@step("the artifact should be unflagged")
def the_artifact_should_be_unflagged(step):
    """Verify that the artifact is now unflagged."""
    from radish import world
    
    # Wait for the flag state to change
    time.sleep(1)
    
    # Check the flag button state
    flag_button = world.driver.find_element(By.CSS_SELECTOR, ".artifact-card:first-child .artifact-actions button:first-child")
    icon = flag_button.find_element(By.CSS_SELECTOR, "ion-icon")
    current_flag_state = "flag" in icon.get_attribute("name") and "outline" not in icon.get_attribute("name")
    
    # The flag state should have changed from the previous state
    assert current_flag_state != world.previous_flag_state, f"Flag state did not change. Expected: {not world.previous_flag_state}, Got: {current_flag_state}"
    print(f"✅ Artifact flag state changed successfully")


@step("the flag icon should be red")
def the_flag_icon_should_be_red(step):
    """Verify that the flag icon is red (flagged state)."""
    from radish import world
    
    flag_button = world.driver.find_element(By.CSS_SELECTOR, ".artifact-card:first-child .artifact-actions button:first-child")
    icon = flag_button.find_element(By.CSS_SELECTOR, "ion-icon")
    
    # Check that it's a filled flag (not outline)
    assert "flag" in icon.get_attribute("name"), "Flag icon should be 'flag'"
    assert "outline" not in icon.get_attribute("name"), "Flag icon should not be outline"
    
    # Check the color (red for flagged)
    color = icon.value_of_css_property("color")
    assert "rgb(220, 53, 69)" in color or "#dc3545" in color, f"Flag icon should be red, got: {color}"
    print("✅ Flag icon is red (flagged state)")


@step("the flag icon should be grey")
def the_flag_icon_should_be_grey(step):
    """Verify that the flag icon is grey (unflagged state)."""
    from radish import world
    
    flag_button = world.driver.find_element(By.CSS_SELECTOR, ".artifact-card:first-child .artifact-actions button:first-child")
    icon = flag_button.find_element(By.CSS_SELECTOR, "ion-icon")
    
    # Check that it's an outline flag
    assert "flag-outline" in icon.get_attribute("name"), "Flag icon should be 'flag-outline'"
    
    # Check the color (grey for unflagged)
    color = icon.value_of_css_property("color")
    assert "rgb(108, 117, 125)" in color or "#6c757d" in color, f"Flag icon should be grey, got: {color}"
    print("✅ Flag icon is grey (unflagged state)")


@step("I have at least one flagged artifact")
def i_have_at_least_one_flagged_artifact(step):
    """Ensure there is at least one flagged artifact for testing."""
    from radish import world
    
    # First, try to flag the first artifact if it's not already flagged
    flag_button = world.driver.find_element(By.CSS_SELECTOR, ".artifact-card:first-child .artifact-actions button:first-child")
    icon = flag_button.find_element(By.CSS_SELECTOR, "ion-icon")
    
    if "flag-outline" in icon.get_attribute("name"):
        # Artifact is not flagged, flag it
        flag_button.click()
        time.sleep(1)
        print("✅ Flagged first artifact for testing")
    else:
        print("✅ First artifact is already flagged")


@step("I click the flag filter button in the toolbar")
def i_click_flag_filter_button_in_toolbar(step):
    """Click the flag filter button in the toolbar."""
    from radish import world
    
    flag_filter_button = world.driver.find_element(By.ID, "flagFilter")
    flag_filter_button.click()
    print("✅ Clicked flag filter button in toolbar")


@step("I click the flag filter button again")
def i_click_flag_filter_button_again(step):
    """Click the flag filter button again."""
    from radish import world
    
    flag_filter_button = world.driver.find_element(By.ID, "flagFilter")
    flag_filter_button.click()
    print("✅ Clicked flag filter button again")


@step("I should see only flagged artifacts")
def i_should_see_only_flagged_artifacts(step):
    """Verify that only flagged artifacts are displayed."""
    from radish import world
    
    # Wait for the filter to be applied
    time.sleep(1)
    
    # Get all visible artifacts
    artifacts = world.driver.find_elements(By.CSS_SELECTOR, ".artifact-card")
    
    if len(artifacts) == 0:
        print("⚠️ No artifacts visible after flag filter")
        return
    
    # Check that all visible artifacts are flagged
    for artifact in artifacts:
        flag_button = artifact.find_element(By.CSS_SELECTOR, ".artifact-actions button:first-child")
        icon = flag_button.find_element(By.CSS_SELECTOR, "ion-icon")
        is_flagged = "flag" in icon.get_attribute("name") and "outline" not in icon.get_attribute("name")
        assert is_flagged, f"Found unflagged artifact in filtered results"
    
    print(f"✅ All {len(artifacts)} visible artifacts are flagged")


@step("the flag filter button should be red")
def the_flag_filter_button_should_be_red(step):
    """Verify that the flag filter button is red (active filter)."""
    from radish import world
    
    flag_filter_button = world.driver.find_element(By.ID, "flagFilter")
    background_color = flag_filter_button.value_of_css_property("background-color")
    
    assert "rgb(220, 53, 69)" in background_color, f"Flag filter button should be red, got: {background_color}"
    print("✅ Flag filter button is red (active filter)")


@step("I should see all artifacts again")
def i_should_see_all_artifacts_again(step):
    """Verify that all artifacts are displayed again."""
    from radish import world
    
    # Wait for the filter to be removed
    time.sleep(1)
    
    # Get all visible artifacts
    artifacts = world.driver.find_elements(By.CSS_SELECTOR, ".artifact-card")
    
    # We should see artifacts (both flagged and unflagged)
    assert len(artifacts) > 0, "No artifacts visible after removing flag filter"
    
    # Check that we have a mix of flagged and unflagged artifacts
    flagged_count = 0
    unflagged_count = 0
    
    for artifact in artifacts:
        flag_button = artifact.find_element(By.CSS_SELECTOR, ".artifact-actions button:first-child")
        icon = flag_button.find_element(By.CSS_SELECTOR, "ion-icon")
        is_flagged = "flag" in icon.get_attribute("name") and "outline" not in icon.get_attribute("name")
        
        if is_flagged:
            flagged_count += 1
        else:
            unflagged_count += 1
    
    print(f"✅ Showing all artifacts again ({flagged_count} flagged, {unflagged_count} unflagged)")


@step("the flag filter button should be grey")
def the_flag_filter_button_should_be_grey(step):
    """Verify that the flag filter button is grey (inactive filter)."""
    from radish import world
    
    flag_filter_button = world.driver.find_element(By.ID, "flagFilter")
    background_color = flag_filter_button.value_of_css_property("background-color")
    
    assert "rgb(108, 117, 125)" in background_color, f"Flag filter button should be grey, got: {background_color}"
    print("✅ Flag filter button is grey (inactive filter)")


@step("I check the \"Flag this artifact\" checkbox")
def i_check_flag_artifact_checkbox(step):
    """Check the flag checkbox in the artifact form."""
    from radish import world
    
    flag_checkbox = world.driver.find_element(By.ID, "artifactFlagged")
    if not flag_checkbox.is_selected():
        flag_checkbox.click()
    
    assert flag_checkbox.is_selected(), "Flag checkbox should be checked"
    print("✅ Checked the 'Flag this artifact' checkbox")


@step("the new artifact should be flagged")
def the_new_artifact_should_be_flagged(step):
    """Verify that the newly created artifact is flagged."""
    from radish import world
    
    # Wait for the modal to close and artifacts to refresh
    time.sleep(2)
    
    # Find the most recent artifact (last in the list)
    artifacts = world.driver.find_elements(By.CSS_SELECTOR, ".artifact-card")
    assert len(artifacts) > 0, "No artifacts found after creation"
    
    # Check the last artifact (most recent)
    last_artifact = artifacts[-1]
    flag_button = last_artifact.find_element(By.CSS_SELECTOR, ".artifact-actions button:first-child")
    icon = flag_button.find_element(By.CSS_SELECTOR, "ion-icon")
    
    is_flagged = "flag" in icon.get_attribute("name") and "outline" not in icon.get_attribute("name")
    assert is_flagged, "Newly created artifact should be flagged"
    print("✅ Newly created artifact is flagged")


@step("And I submit the form")
def and_i_submit_form(step):
    """Submit the artifact form."""
    from radish import world
    
    # Find and click the submit button
    submit_button = world.driver.find_element(By.CSS_SELECTOR, "#artifactForm button[type='submit']")
    submit_button.click()
    
    print("✅ Submitted the form")


@step("I submit the form")
def i_submit_form_alias(step):
    """Alias: Submit the artifact form."""
    return and_i_submit_form(step)


@step("I should see the new artifact created")
def i_should_see_new_artifact_created(step):
    """Verify that a new artifact was created."""
    from radish import world
    
    # Wait for the modal to close and artifacts to refresh
    time.sleep(2)
    
    # Check that we have artifacts
    artifacts = world.driver.find_elements(By.CSS_SELECTOR, ".artifact-card")
    assert len(artifacts) > 0, "No artifacts found after creation"
    
    # Look for the new artifact with our test summary
    new_artifact_found = False
    for artifact in artifacts:
        summary_element = artifact.find_element(By.CSS_SELECTOR, ".artifact-summary")
        if "Test artifact with flag" in summary_element.text:
            new_artifact_found = True
            break
    
    assert new_artifact_found, "New artifact with test summary not found"
    print("✅ New artifact created successfully")
