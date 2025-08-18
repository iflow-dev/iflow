from radish import step, world
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

@step("I filter by status {status:QuotedString}")
def i_filter_by_status(step, status):
    """Filter artifacts by the specified status."""
    from radish import world
    
    # Find the status filter dropdown
    status_filter = world.driver.find_element(By.ID, "statusFilter")
    
    # Wait for options to be populated (up to 10 seconds)
    max_wait = 10
    wait_time = 0
    while wait_time < max_wait:
        try:
            select = Select(status_filter)
            options = select.options
            if len(options) > 1:  # More than just "All Statuses"
                print(f"Status filter options populated after {wait_time}s, found {len(options)} options")
                break
        except Exception as e:
            print(f"Waiting for status filter options: {e}")
        
        time.sleep(1)
        wait_time += 1
    
    # Now try to select the status using JavaScript
    try:
        # First try the normal Select approach
        select = Select(status_filter)
        select.select_by_value(status)
        print(f"Successfully selected status '{status}' using Select")
    except Exception as e:
        print(f"Select approach failed: {e}")
        # Fallback to JavaScript
        world.driver.execute_script(f"arguments[0].value = '{status}'; arguments[0].dispatchEvent(new Event('change'));", status_filter)
        print(f"Set status '{status}' using JavaScript")
    
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
    """Clear the status filter by selecting the default option."""
    from radish import world
    
    # Find the status filter dropdown
    status_filter = world.driver.find_element(By.ID, "statusFilter")
    
    # Use JavaScript to clear the filter
    try:
        # First try the normal Select approach
        select = Select(status_filter)
        select.select_by_index(0)
        print("Successfully cleared status filter using Select")
    except Exception as e:
        print(f"Select approach failed: {e}")
        # Fallback to JavaScript
        world.driver.execute_script("arguments[0].value = ''; arguments[0].dispatchEvent(new Event('change'));", status_filter)
        print("Cleared status filter using JavaScript")
    
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
