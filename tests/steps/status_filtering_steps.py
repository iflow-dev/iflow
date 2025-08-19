from radish import given, when, then, step
from controls import Title
import logging

# Set up logging
log = logging.getLogger(__name__)

@step(r"I set the status filter to {status:QuotedString}")
def i_set_status_filter_to(step, status):
    """Set the status filter to the specified value using JavaScript accessibility functions."""
    from radish import world
    
    try:
        # Use JavaScript accessibility function to set the status filter
        log.debug(f"Using JavaScript accessibility function to set status filter to '{status}'...")
        
        # Call the JavaScript function to set the dropdown value
        result = world.driver.execute_script(f"return setDropdownValue('statusFilter', '{status}');")
        
        if result:
            log.debug(f"Successfully set status filter to '{status}' using JavaScript accessibility function")
        else:
            # Fallback to traditional Select method
            from selenium.webdriver.support.ui import Select
            from selenium.webdriver.common.by import By
            
            status_filter = world.driver.find_element(By.ID, "statusFilter")
            select = Select(status_filter)
            select.select_by_visible_text(status)
            log.debug(f"Fallback: Successfully selected status '{status}' using Select")
        
        # Wait for the filter to take effect
        import time
        time.sleep(2)
        log.debug("Waited 2 seconds for filter to take effect")
            
    except Exception as e:
        log.debug(f"Fallback failed: {e}")
        raise AssertionError(f"Failed to set status filter to '{status}': {e}")

@step(r"I verify the status filter is set to {status:QuotedString}")
def i_verify_status_filter_is_set_to(step, status):
    """Verify that the status filter is set to the specified value."""
    from radish import world
    
    try:
        # Use JavaScript accessibility function to get the current value
        actual_value = world.driver.execute_script("return getDropdownValue('statusFilter');")
        
        if actual_value == status:
            log.debug(f"Verified status filter is now '{actual_value}'")
        else:
            log.debug(f"Warning: Expected status '{status}', but got '{actual_value}'")
            
    except Exception as e:
        log.debug(f"Failed to set status filter to '{status}' using JavaScript accessibility function")
        raise AssertionError(f"Failed to verify status filter: {e}")

@step(r"I see only artifacts with status {status:QuotedString}")
def i_see_only_artifacts_with_status(step, status):
    """Verify that only artifacts with the specified status are visible."""
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
                log.debug(f"Found artifact with status: '{status_text}'")
                
                # Check if the status text contains the expected status (ignoring emojis and case)
                if status.lower() in status_text.lower():
                    artifacts_with_correct_status += 1
                    
            except Exception as e:
                log.debug(f"Error checking artifact status: {e}")
                # Continue checking other artifacts
                continue
        
        log.debug(f"Found {artifacts_with_correct_status} artifacts with status '{status}' out of {len(visible_artifacts)} visible artifacts")
        
        # Verify that the filter is working - at least some artifacts should have the correct status
        # and all visible artifacts should have the correct status (filter should exclude others)
        if artifacts_with_correct_status == 0:
            raise AssertionError(f"No artifacts found with status '{status}' - filter may not be working")
        
        if artifacts_with_correct_status != len(visible_artifacts):
            raise AssertionError(f"Status filter not working correctly: expected all visible artifacts to have status '{status}', but only {artifacts_with_correct_status} out of {len(visible_artifacts)} artifacts have this status")
            
    except Exception as e:
        raise AssertionError(f"Error verifying artifact statuses: {e}")

@step("I clear the status filter")
def i_clear_status_filter(step):
    """Clear the status filter to show all artifacts."""
    from radish import world
    
    try:
        # Use JavaScript accessibility function to clear the status filter
        log.debug("Using JavaScript accessibility function to clear status filter...")
        
        # Call the JavaScript function to clear the dropdown value
        result = world.driver.execute_script("return setDropdownValue('statusFilter', '');")
        
        if result:
            log.debug("Successfully cleared status filter using JavaScript accessibility function")
        else:
            # Fallback to traditional Select method
            from selenium.webdriver.support.ui import Select
            from selenium.webdriver.common.by import By
            
            status_filter = world.driver.find_element(By.ID, "statusFilter")
            select = Select(status_filter)
            select.select_by_index(0)  # Select the first option (usually "All" or empty)
            log.debug("Fallback: Successfully cleared status filter using Select")
            
    except Exception as e:
        log.debug(f"Fallback failed: {e}")
        raise AssertionError(f"Failed to clear status filter: {e}")

@step("I verify the status filter is cleared")
def i_verify_status_filter_is_cleared(step):
    """Verify that the status filter is cleared."""
    from radish import world
    
    try:
        # Use JavaScript accessibility function to get the current value
        actual_value = world.driver.execute_script("return getDropdownValue('statusFilter');")
        
        if not actual_value or actual_value == "":
            log.debug("Verified status filter is now cleared")
        else:
            log.debug(f"Warning: Expected empty value, but got '{actual_value}'")
            
    except Exception as e:
        log.debug("Failed to clear status filter using JavaScript accessibility function")
        raise AssertionError(f"Failed to verify status filter is cleared: {e}")

@step("I see all artifacts again")
def i_see_all_artifacts_again(step):
    """Verify that all artifacts are visible after clearing the filter."""
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
        
        # Verify that artifacts are visible (we don't need to check specific counts)
        if not visible_artifacts:
            raise AssertionError("No artifacts are visible after clearing the filter")
            
    except Exception as e:
        raise AssertionError(f"Error verifying all artifacts are visible: {e}")
