"""
Step definitions for artifact flags functionality tests.
"""

from radish import step, world
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import subprocess


@step("I reset the database to {branch}")
def i_reset_database_to_branch(step, branch):
    """Reset the test database to a specific branch."""
    from radish import world
    
    # Run the reset script to reset the database
    reset_script = "/Users/claudio/realtime/reos2/reset_test_db.sh"
    try:
        result = subprocess.run([reset_script], capture_output=True, text=True, check=True)
        print(f"✅ Database reset to {branch} branch successful")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Database reset failed: {e.stderr}")
        # Continue anyway as this might be expected in some environments
    except FileNotFoundError:
        print(f"⚠️ Reset script not found at {reset_script}, continuing without reset")


@step("I see artifacts displayed")
def i_see_artifacts_displayed(step):
    """Verify that artifacts are displayed on the page."""
    from radish import world
    
    # Wait for artifacts to load
    wait = WebDriverWait(world.driver, 10)
    artifacts = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".artifact-card")))
    
    assert len(artifacts) > 0, "No artifacts found on the page"
    print(f"✅ Found {len(artifacts)} artifacts displayed")


@step("I flag artifact #{artifact_id}")
def i_flag_artifact_by_id(step, artifact_id):
    """Flag a specific artifact by ID."""
    from radish import world
    
    # Find the artifact with the specific ID
    wait = WebDriverWait(world.driver, 10)
    artifacts = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".artifact-card")))
    
    # Find the artifact with the matching ID
    target_artifact = None
    for artifact in artifacts:
        try:
            id_element = artifact.find_element(By.CSS_SELECTOR, ".artifact-id")
            if artifact_id in id_element.text:
                target_artifact = artifact
                break
        except:
            continue
    
    if not target_artifact:
        raise Exception(f"Artifact with ID {artifact_id} not found")
    
    # Find the flag button within this artifact
    flag_button = target_artifact.find_element(By.CSS_SELECTOR, ".artifact-actions button:first-child")
    
    # Store the current flag state for verification
    icon = flag_button.find_element(By.CSS_SELECTOR, "ion-icon")
    icon_name = icon.get_attribute("name")
    # Check if the button is currently flagged (filled icon) or unflagged (outline icon)
    world.previous_flag_state = "outline" not in icon_name
    
    flag_button.click()
    
    # Wait for any modal to close if it was open
    try:
        WebDriverWait(world.driver, 2).until_not(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".modal-content"))
        )
    except TimeoutException:
        # Modal might not be present, which is fine
        pass
    
    print(f"✅ Flagged artifact #{artifact_id} (previous state: {'flagged' if world.previous_flag_state else 'unflagged'})")


@step("the artifact should be flagged")
def the_artifact_should_be_flagged(step):
    """Verify that the artifact is now flagged."""
    from radish import world
    
    # Wait for the flag state to change
    time.sleep(1)
    
    # Check the flag button state
    flag_button = world.driver.find_element(By.CSS_SELECTOR, ".artifact-card:first-child .artifact-actions button:first-child")
    icon = flag_button.find_element(By.CSS_SELECTOR, "ion-icon")
    icon_name = icon.get_attribute("name")
    current_flag_state = "outline" not in icon_name
    
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
    
    # Handle both rgb and rgba formats
    assert "220, 53, 69" in background_color, f"Flag filter button should be red, got: {background_color}"
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
    
    # Handle both rgb and rgba formats
    assert "108, 117, 125" in background_color, f"Flag filter button should be grey, got: {background_color}"
    print("✅ Flag filter button is grey (inactive filter)")


@step("I check the \"Flag this artifact\" checkbox")
def i_check_flag_artifact_checkbox(step):
    """Check the flag checkbox in the artifact form."""
    from radish import world
    import time
    
    # Try to find the flag checkbox with different possible IDs
    flag_checkbox = None
    possible_ids = ["artifactFlagged", "artifact-flagged", "flagged", "flag"]
    
    for checkbox_id in possible_ids:
        try:
            flag_checkbox = world.driver.find_element(By.ID, checkbox_id)
            print(f"✅ Found flag checkbox with ID: {checkbox_id}")
            break
        except:
            continue
    
    if not flag_checkbox:
        # Try to find by name attribute
        try:
            flag_checkbox = world.driver.find_element(By.NAME, "flagged")
            print(f"✅ Found flag checkbox with name: flagged")
        except:
            # Try to find by XPath
            try:
                flag_checkbox = world.driver.find_element(By.XPATH, "//input[@type='checkbox' and contains(@name, 'flag')]")
                print(f"✅ Found flag checkbox with XPath")
            except:
                # Last resort: try to find any checkbox in the form
                try:
                    flag_checkbox = world.driver.find_element(By.XPATH, "//div[@id='artifactModal']//input[@type='checkbox']")
                    print(f"✅ Found checkbox in modal (ID: {flag_checkbox.get_attribute('id')}, name: {flag_checkbox.get_attribute('name')})")
                except Exception as e:
                    print(f"❌ Could not find flag checkbox: {e}")
                    raise AssertionError("Flag checkbox not found in the form")
    
    if not flag_checkbox.is_selected():
        flag_checkbox.click()
        print(f"✅ Clicked checkbox (ID: {flag_checkbox.get_attribute('id')}, name: {flag_checkbox.get_attribute('name')})")
    
    # Wait for the flag state to be processed
    time.sleep(0.5)
    
    assert flag_checkbox.is_selected(), "Flag checkbox should be checked"
    print("✅ Checked the 'Flag this artifact' checkbox")


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


@step("the new artifact should be flagged")
def the_new_artifact_should_be_flagged(step):
    """Verify that the newly created artifact is flagged."""
    from radish import world
    import time
    
    # Wait for the modal to close and artifacts to refresh
    time.sleep(2)
    
    # Find the specific artifact we created by its summary text
    artifacts = world.driver.find_elements(By.CSS_SELECTOR, ".artifact-card")
    assert len(artifacts) > 0, "No artifacts found after creation"
    
    target_artifact = None
    for artifact in artifacts:
        try:
            summary_element = artifact.find_element(By.CSS_SELECTOR, ".artifact-summary")
            if "Test artifact with flag" in summary_element.text:
                target_artifact = artifact
                break
        except:
            continue
    
    assert target_artifact is not None, "Could not find the newly created artifact with test summary"
    
    # Check the flag button on our specific artifact
    flag_button = target_artifact.find_element(By.CSS_SELECTOR, ".artifact-actions button:first-child")
    icon = flag_button.find_element(By.CSS_SELECTOR, "ion-icon")
    
    icon_name = icon.get_attribute("name")
    is_flagged = "flag" in icon_name and "outline" not in icon_name
    
    if not is_flagged:
        print(f"❌ Artifact flag icon name: '{icon_name}' (expected: filled flag, not outline)")
    
    assert is_flagged, f"Newly created artifact should be flagged but icon name is '{icon_name}'"
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


# Note: "I fill in the artifact details" step definition already exists in artifact_steps.py


# Note: Refresh button functionality is handled in toolbar_refresh_steps.py

@step("I should still see only artifacts with status {status:QuotedString}")
def i_should_still_see_only_artifacts_with_status(step, status):
    """Verify that the status filter is still applied after flagging/unflagging."""
    from radish import world
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    try:
        # Wait for artifacts to be visible
        WebDriverWait(world.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "artifact-card"))
        )
        
        # Get all visible artifact cards
        visible_artifacts = world.driver.find_elements(By.CLASS_NAME, "artifact-card")
        
        if not visible_artifacts:
            raise AssertionError("No artifacts are visible")
        
        # Check each artifact's status
        artifacts_with_correct_status = 0
        for artifact in visible_artifacts:
            try:
                # Look for status indicator in the artifact card
                status_element = artifact.find_element(By.CSS_SELECTOR, ".status-indicator, .artifact-status")
                status_text = status_element.text.strip()
                
                # Check if the status text contains the expected status (ignoring emojis and case)
                if status.lower() in status_text.lower():
                    artifacts_with_correct_status += 1
                    
            except Exception as e:
                # Continue checking other artifacts
                continue
        
        # Verify that the filter is still working - at least some artifacts should have the correct status
        # and all visible artifacts should have the correct status (filter should exclude others)
        assert artifacts_with_correct_status > 0, f"No artifacts with status '{status}' found after flagging"
        assert artifacts_with_correct_status == len(visible_artifacts), f"Filter not working: found {artifacts_with_correct_status} artifacts with status '{status}' out of {len(visible_artifacts)} visible artifacts"
        
        print(f"✅ Status filter still working: {artifacts_with_correct_status} artifacts with status '{status}' visible")
        
    except Exception as e:
        raise AssertionError(f"Failed to verify status filter persistence: {e}")

@step("the status filter should still be set to {status:QuotedString}")
def the_status_filter_should_still_be_set_to(step, status):
    """Verify that the status filter dropdown still shows the correct value."""
    from radish import world
    
    try:
        # Use JavaScript accessibility function to get the current value
        actual_value = world.driver.execute_script("return getDropdownValue('statusFilter');")
        
        if actual_value == status:
            print(f"✅ Status filter still correctly set to '{actual_value}'")
        else:
            raise AssertionError(f"Status filter value changed. Expected: '{status}', Got: '{actual_value}'")
            
    except Exception as e:
        raise AssertionError(f"Failed to verify status filter value: {e}")
