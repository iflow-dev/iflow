"""
Step definitions for refresh filter functionality.
"""

from radish import given, when, then
from selenium.webdriver.common.by import By
from bdd.controls.dropdown import DropdownFactory





@given("I filter for type {filter_value}")
def filter_for_type(step, filter_value):
    """Apply a type filter with the specified value."""
    from radish import world
    from time import sleep
    
    # Strip quotes from the filter value
    filter_value = filter_value.strip('"')
    
    print(f"Debug: Setting up type filter for '{filter_value}'")
    
    # Use the dropdown control to select the option
    type_dropdown = Dropdown('type')
    type_dropdown.select_option(world.driver, filter_value)
    
    # Wait for the filtering to be applied
    sleep(2)
    
    # Verify that filtering worked by checking the number of displayed artifacts
    artifacts = world.driver.find_elements(By.CSS_SELECTOR, ".artifact-card")
    print(f"Debug: Found {len(artifacts)} artifacts after applying type filter '{filter_value}'")


@given("I filter for status {filter_value}")
def filter_for_status(step, filter_value):
    """Apply a status filter with the specified value."""
    from radish import world
    from time import sleep
    
    # Strip quotes from the filter value
    filter_value = filter_value.strip('"')
    
    print(f"Debug: Setting up status filter for '{filter_value}'")
    
    # Use the dropdown control to select the option
    status_dropdown = Dropdown('status')
    status_dropdown.select_option(world.driver, filter_value)
    
    # Wait for the filtering to be applied
    sleep(2)
    
    # Verify that filtering worked by checking the number of displayed artifacts
    artifacts = world.driver.find_elements(By.CSS_SELECTOR, ".artifact-card")
    print(f"Debug: Found {len(artifacts)} artifacts after applying status filter '{filter_value}'")


@when("I refresh the view")
def refresh_the_view(step):
    """Refresh the view by clicking the refresh button."""
    from radish import world
    from time import sleep
    
    # Close any open dropdowns by clicking outside of them
    try:
        body = world.driver.find_element(By.TAG_NAME, "body")
        body.click()
        sleep(0.5)
    except:
        pass
    
    # Find and click the refresh button
    refresh_button = world.driver.find_element(By.CSS_SELECTOR, "button[title='Refresh artifacts']")
    refresh_button.click()
    
    # Wait for refresh to complete
    sleep(2)


@then("I see the type filter is set to {expected_value}")
def see_type_filter_set_to(step, expected_value):
    """Check that the type filter shows the expected value."""
    from radish import world
    
    # Strip quotes from expected value
    expected_value = expected_value.strip('"')
    
    # Use the dropdown control to get the selected value
    type_dropdown = Dropdown('type')
    actual_value = type_dropdown.get_selected_value(world.driver)
    
    print(f"Debug: Type filter shows '{actual_value}', expected '{expected_value}'")
    
    # Check if the expected value is in the actual text (case insensitive)
    assert expected_value.lower() in actual_value.lower(), f"Type filter should show '{expected_value}', but shows '{actual_value}'"


@then("I see the status filter is set to {expected_value}")
def see_status_filter_set_to(step, expected_value):
    """Check that the status filter shows the expected value."""
    from radish import world
    
    # Strip quotes from expected value
    expected_value = expected_value.strip('"')
    
    # Use the dropdown control to get the selected value
    status_dropdown = Dropdown('status')
    actual_value = status_dropdown.get_selected_value(world.driver)
    
    print(f"Debug: Status filter shows '{actual_value}', expected '{expected_value}'")
    
    # Check if the expected value is in the actual text (case insensitive)
    assert expected_value.lower() in actual_value.lower(), f"Status filter should show '{expected_value}', but shows '{actual_value}'"


@then("I only see requirement items")
def only_see_requirement_items(step):
    """Check that only requirement items are displayed."""
    from radish import world
    
    # Check that artifacts are filtered to show only requirements
    artifacts = world.driver.find_elements(By.CSS_SELECTOR, ".artifact-card")
    
    # Should see some artifacts
    assert len(artifacts) > 0, "Should see some requirement items"
    
    # Check that all artifacts are of type "requirement"
    for artifact in artifacts:
        artifact_text = artifact.text.lower()
        assert "requirement" in artifact_text, f"Artifact should be of type 'requirement': {artifact_text[:100]}"


@then("I only see requirement items with open status")
def only_see_requirement_items_with_open_status(step):
    """Check that only requirement items with open status are displayed."""
    from radish import world
    
    # Check that artifacts are filtered to show only requirements with open status
    artifacts = world.driver.find_elements(By.CSS_SELECTOR, ".artifact-card")
    
    # Should see some artifacts
    assert len(artifacts) > 0, "Should see some requirement items with open status"
    
    # Check that all artifacts are of type "requirement" and have "open" status
    for artifact in artifacts:
        artifact_text = artifact.text.lower()
        
        # Should contain "requirement" (type filter)
        assert "requirement" in artifact_text, f"Artifact should be of type 'requirement': {artifact_text[:100]}"
        
        # Should contain "open" (status filter)
        assert "open" in artifact_text, f"Artifact should have 'open' status: {artifact_text[:100]}"
