from radish import step, world
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

@step("I filter by status {status:QuotedString}")
def i_filter_by_status(step, status):
    """Filter artifacts by the specified status using JavaScript accessibility functions."""
    from radish import world
    
    # Use the new JavaScript accessibility function to set the status filter
    print(f"Using JavaScript accessibility function to set status filter to '{status}'...")
    
    result = world.driver.execute_script(f"""
        if (typeof setDropdownValue === 'function') {{
            return setDropdownValue('statusFilter', '{status}');
        }} else {{
            console.error('setDropdownValue function not available');
            return false;
        }}
    """)
    
    if result:
        print(f"Successfully set status filter to '{status}' using JavaScript accessibility function")
        
        # Verify the value was set correctly
        actual_value = world.driver.execute_script(f"""
            if (typeof getDropdownValue === 'function') {{
                return getDropdownValue('statusFilter');
            }} else {{
                return null;
            }}
        """)
        
        if actual_value == status:
            print(f"Verified status filter is now '{actual_value}'")
        else:
            print(f"Warning: Expected status '{status}', but got '{actual_value}'")
    else:
        print(f"Failed to set status filter to '{status}' using JavaScript accessibility function")
        # Fallback to old method
        try:
            status_filter = world.driver.find_element(By.ID, "statusFilter")
            select = Select(status_filter)
            select.select_by_value(status)
            print(f"Fallback: Successfully selected status '{status}' using Select")
        except Exception as e:
            print(f"Fallback failed: {e}")
            raise Exception(f"Could not set status filter to '{status}'")
    
    # Wait for filtering to complete
    time.sleep(1)

@step("I see artifacts with status {status:QuotedString}")
def i_see_artifacts_with_status(step, status):
    """Verify that artifacts with the specified status are displayed."""
    from radish import world
    
    # Wait for filtering to complete
    time.sleep(1)
    
    # Find all visible artifact cards
    artifact_cards = world.driver.find_elements(By.CLASS_NAME, "artifact-card")
    
    # Check that at least one artifact is displayed
    visible_artifacts = [card for card in artifact_cards if card.is_displayed()]
    assert len(visible_artifacts) > 0, f"No artifacts are visible after filtering by status '{status}'"
    
    # Check that at least some artifacts have the correct status
    artifacts_with_correct_status = 0
    for artifact in visible_artifacts:
        # Look for status indicator in the artifact card
        try:
            # Find the status element specifically
            status_element = artifact.find_element(By.CLASS_NAME, "artifact-status")
            status_text = status_element.text.lower()
            print(f"Found artifact with status: '{status_text}'")
            
            # Check if the status contains our expected status (case insensitive)
            if status.lower() in status_text:
                artifacts_with_correct_status += 1
        except Exception as e:
            print(f"Error checking artifact status: {e}")
            continue
    
    # Verify that we found at least some artifacts with the correct status
    assert artifacts_with_correct_status > 0, f"No artifacts found with status '{status}' among {len(visible_artifacts)} visible artifacts"
    print(f"Found {artifacts_with_correct_status} artifacts with status '{status}' out of {len(visible_artifacts)} visible artifacts")

@step("I clear the status filter")
def i_clear_the_status_filter(step):
    """Clear the status filter using JavaScript accessibility functions."""
    from radish import world
    
    # Use the new JavaScript accessibility function to clear the status filter
    print("Using JavaScript accessibility function to clear status filter...")
    
    result = world.driver.execute_script(f"""
        if (typeof setDropdownValue === 'function') {{
            return setDropdownValue('statusFilter', '');
        }} else {{
            console.error('setDropdownValue function not available');
            return false;
        }}
    """)
    
    if result:
        print("Successfully cleared status filter using JavaScript accessibility function")
        
        # Verify the value was cleared
        actual_value = world.driver.execute_script(f"""
            if (typeof getDropdownValue === 'function') {{
                return getDropdownValue('statusFilter');
            }} else {{
                return null;
            }}
        """)
        
        if actual_value == "":
            print("Verified status filter is now cleared")
        else:
            print(f"Warning: Expected empty value, but got '{actual_value}'")
    else:
        print("Failed to clear status filter using JavaScript accessibility function")
        # Fallback to old method
        try:
            status_filter = world.driver.find_element(By.ID, "statusFilter")
            select = Select(status_filter)
            select.select_by_index(0)
            print("Fallback: Successfully cleared status filter using Select")
        except Exception as e:
            print(f"Fallback failed: {e}")
            raise Exception("Could not clear status filter")
    
    # Wait for filtering to complete
    time.sleep(1)

@step("I see all artifacts again")
def i_see_all_artifacts_again(step):
    """Verify that all artifacts are displayed after clearing the filter."""
    from radish import world
    
    # Wait for filtering to complete
    time.sleep(1)
    
    # Find all visible artifact cards
    artifact_cards = world.driver.find_elements(By.CLASS_NAME, "artifact-card")
    
    # Check that artifacts are displayed (we should see more than just filtered results)
    visible_artifacts = [card for card in artifact_cards if card.is_displayed()]
    assert len(visible_artifacts) > 0, "No artifacts are visible after clearing the filter"
    
    # Verify that the status filter is reset to default
    status_filter = world.driver.find_element(By.ID, "statusFilter")
    select = Select(status_filter)
    selected_option = select.first_selected_option
    selected_value = selected_option.get_attribute("value")
    assert selected_option.text == "All Statuses" or selected_value == "", f"Status filter not reset: {selected_option.text}"
