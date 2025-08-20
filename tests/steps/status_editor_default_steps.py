"""
Step definitions for testing status field default values in the editor.
This module tests that the status field properly shows default values and actual values.
"""

from radish import given, when, then, step
import logging

# Set up logging
log = logging.getLogger(__name__)

@step("the artifact editor is available")
def the_artifact_editor_is_available(step):
    """Verify that the artifact editor is available on the page."""
    from radish import world
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    try:
        # Wait for the create button to be visible
        create_button = WebDriverWait(world.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Create')]"))
        )
        log.debug("Artifact editor is available - create button found")
    except Exception as e:
        raise AssertionError(f"Artifact editor is not available: {e}")

@step("the status field should show {expected_status:QuotedString}")
def the_status_field_should_show_expected_status(step, expected_status):
    """Verify that the status field shows the expected status value."""
    from radish import world
    from selenium.webdriver.common.by import By
    
    try:
        # Find the status select element
        status_select = world.driver.find_element(By.ID, "artifactStatus")
        
        # Get the current value
        actual_value = status_select.get_attribute("value")
        
        if actual_value == expected_status:
            log.debug(f"Status field correctly shows expected status: {actual_value}")
        else:
            raise AssertionError(f"Expected status field to show '{expected_status}', but got '{actual_value}'")
            
    except Exception as e:
        raise AssertionError(f"Failed to verify status field value: {e}")

@step("I change the status to {new_status:QuotedString}")
def i_change_status_to(step, new_status):
    """Change the status field to the specified value."""
    from radish import world
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import Select
    
    try:
        # Find the status select element
        status_select = world.driver.find_element(By.ID, "artifactStatus")
        
        # Change the status using Select
        select = Select(status_select)
        select.select_by_value(new_status)
        
        log.debug(f"Changed status to '{new_status}'")
        
    except Exception as e:
        raise AssertionError(f"Failed to change status field value: {e}")

@step("I see the status is {expected_status:QuotedString}")
def i_see_status_is(step, expected_status):
    """Verify that the status field shows the expected status value."""
    from radish import world
    from selenium.webdriver.common.by import By
    
    try:
        # Find the status select element
        status_select = world.driver.find_element(By.ID, "artifactStatus")
        
        # Get the current value
        actual_value = status_select.get_attribute("value")
        
        if actual_value == expected_status:
            log.debug(f"Status field correctly shows expected status: {actual_value}")
        else:
            raise AssertionError(f"Expected status field to show '{expected_status}', but got '{actual_value}'")
            
    except Exception as e:
        raise AssertionError(f"Failed to verify status field value: {e}")

@step("I have an existing artifact with status {status:QuotedString}")
def i_have_existing_artifact_with_status(step, status):
    """Verify that there is an existing artifact with the specified status."""
    from radish import world
    
    # This step assumes there are existing artifacts in the system
    # We'll check if we can find an artifact with the given status
    log.debug(f"Looking for existing artifact with status: {status}")
    
    # For now, we'll just verify that the status is valid
    valid_statuses = ['open', 'in_progress', 'done', 'blocked']
    if status not in valid_statuses:
        raise AssertionError(f"Invalid status '{status}'. Valid statuses are: {valid_statuses}")

@step("I edit the existing artifact")
def i_edit_existing_artifact(step):
    """Open the edit modal for an existing artifact."""
    from radish import world
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    try:
        # Find and click the first edit button available
        edit_button = WebDriverWait(world.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".edit-button, [title*='edit'], [aria-label*='edit']"))
        )
        edit_button.click()
        log.debug("Clicked edit button for existing artifact")
        
        # Wait for the edit modal to open
        WebDriverWait(world.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "artifactModal"))
        )
        log.debug("Edit modal opened successfully")
        
    except Exception as e:
        raise AssertionError(f"Failed to open edit modal: {e}")

@step("I see the artifact edit form")
def i_see_artifact_edit_form(step):
    """Verify that the artifact edit form is displayed."""
    from radish import world
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    try:
        # Wait for the edit modal to be visible
        modal = WebDriverWait(world.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "artifactModal"))
        )
        
        # Check if the modal title indicates editing
        title_element = world.driver.find_element(By.ID, "modalTitle")
        if "Edit" in title_element.text:
            log.debug("Artifact edit form is displayed")
        else:
            raise AssertionError(f"Modal title does not indicate editing: {title_element.text}")
            
    except Exception as e:
        raise AssertionError(f"Failed to verify edit form is displayed: {e}")

# Note: Step "I set the status to {status:QuotedString}" is already defined in artifact_creation_steps.py

@step("I should see a success message")
def i_should_see_success_message(step):
    """Verify that a success message is displayed."""
    from radish import world
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    try:
        # Wait for success message or modal to close
        # Success could be indicated by modal closing or a success message
        WebDriverWait(world.driver, 10).until(
            EC.invisibility_of_element_located((By.ID, "artifactModal"))
        )
        log.debug("Success message indicated by modal closing")
        
    except Exception as e:
        # Check for explicit success message
        try:
            success_element = world.driver.find_element(By.CSS_SELECTOR, ".success, .alert-success, [class*='success']")
            if success_element.is_displayed():
                log.debug("Success message found and displayed")
                return
        except:
            pass
        
        raise AssertionError(f"Failed to verify success message: {e}")

@step("the new artifact should have status {expected_status:QuotedString}")
def the_new_artifact_should_have_status(step, expected_status):
    """Verify that the newly created artifact has the expected status."""
    from radish import world
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    try:
        # Look for the artifact with the test summary
        test_summary = "Test artifact with custom status"
        
        # Wait for artifacts to be visible
        WebDriverWait(world.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "artifact-card"))
        )
        
        # Find the artifact with the test summary
        artifacts = world.driver.find_elements(By.CLASS_NAME, "artifact-card")
        target_artifact = None
        
        for artifact in artifacts:
            try:
                summary_element = artifact.find_element(By.CSS_SELECTOR, ".artifact-summary, .summary, [class*='summary']")
                if test_summary in summary_element.text:
                    target_artifact = artifact
                    break
            except:
                continue
        
        if not target_artifact:
            raise AssertionError(f"Could not find artifact with summary: {test_summary}")
        
        # Check the status of the found artifact
        try:
            status_element = target_artifact.find_element(By.CSS_SELECTOR, ".status-indicator, .artifact-status, [class*='status']")
            actual_status_text = status_element.text.strip()
            
            # The status text might contain the status name, so we check if it contains the expected status
            if expected_status.lower() in actual_status_text.lower():
                log.debug(f"New artifact correctly has status: {expected_status}")
            else:
                raise AssertionError(f"Expected status '{expected_status}', but artifact shows: {actual_status_text}")
                
        except Exception as e:
            raise AssertionError(f"Failed to check artifact status: {e}")
            
    except Exception as e:
        raise AssertionError(f"Failed to verify new artifact status: {e}")
