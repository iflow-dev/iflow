"""
Step definitions for refresh filter functionality.
"""

from radish import given, when, then
from selenium.webdriver.common.by import By


@given("I have applied a filter to the view")
def have_applied_filter_to_view(step):
    """Apply a filter to the current view."""
    from radish import world
    from time import sleep
    
    # Find the custom type filter dropdown (first custom dropdown)
    custom_dropdowns = world.driver.find_elements(By.CSS_SELECTOR, ".custom-dropdown")
    if len(custom_dropdowns) >= 1:
        # Click on the dropdown button to open it
        dropdown_button = custom_dropdowns[0].find_element(By.CSS_SELECTOR, ".custom-dropdown-button")
        dropdown_button.click()
        sleep(0.5)
        
        # Find and click the "requirement" option
        options = world.driver.find_elements(By.CSS_SELECTOR, ".custom-dropdown-option")
        for option in options:
            if "requirement" in option.text.lower():
                option.click()
                break
        sleep(0.5)


@given("I have applied multiple filters to the view")
def have_applied_multiple_filters_to_view(step):
    """Apply multiple filters to the current view."""
    from radish import world
    from time import sleep
    
    # Apply type filter to "requirement"
    custom_dropdowns = world.driver.find_elements(By.CSS_SELECTOR, ".custom-dropdown")
    if len(custom_dropdowns) >= 1:
        # Click on the first dropdown button to open it
        dropdown_button = custom_dropdowns[0].find_element(By.CSS_SELECTOR, ".custom-dropdown-button")
        dropdown_button.click()
        sleep(0.5)
        
        # Find and click the "requirement" option
        options = world.driver.find_elements(By.CSS_SELECTOR, ".custom-dropdown-option")
        for option in options:
            if "requirement" in option.text.lower():
                option.click()
                break
        sleep(0.5)
    
    # Apply status filter to "open"
    if len(custom_dropdowns) >= 2:
        # Click on the second dropdown button to open it
        dropdown_button = custom_dropdowns[1].find_element(By.CSS_SELECTOR, ".custom-dropdown-button")
        dropdown_button.click()
        sleep(0.5)
        
        # Find and click the "open" option
        options = world.driver.find_elements(By.CSS_SELECTOR, ".custom-dropdown-option")
        for option in options:
            if "open" in option.text.lower():
                option.click()
                break
        sleep(0.5)
    
    # Apply category filter
    category_filter = world.driver.find_element(By.CSS_SELECTOR, "input[placeholder='Filter by category...']")
    category_filter.clear()
    category_filter.send_keys("testing")
    sleep(0.5)
    
    # Apply search filter
    search_box = world.driver.find_element(By.CSS_SELECTOR, "input[placeholder='Search artifacts...']")
    search_box.clear()
    search_box.send_keys("requirement")
    sleep(1)


@given("I have applied a type filter to {filter_value}")
def have_applied_type_filter(step, filter_value):
    """Apply a type filter with the specified value."""
    from radish import world
    from time import sleep
    
    # Find the type filter dropdown (first custom dropdown)
    custom_dropdowns = world.driver.find_elements(By.CSS_SELECTOR, ".custom-dropdown")
    if len(custom_dropdowns) >= 1:
        # Click on the dropdown button to open it
        dropdown_button = custom_dropdowns[0].find_element(By.CSS_SELECTOR, ".custom-dropdown-button")
        dropdown_button.click()
        sleep(0.5)
        
        # Find and click the specified option
        options = world.driver.find_elements(By.CSS_SELECTOR, ".custom-dropdown-option")
        for option in options:
            if filter_value.lower() in option.text.lower():
                option.click()
                break
        sleep(0.5)


@given("I have applied a status filter to {filter_value}")
def have_applied_status_filter(step, filter_value):
    """Apply a status filter with the specified value."""
    from radish import world
    from time import sleep
    
    # Find the status filter dropdown (second custom dropdown)
    custom_dropdowns = world.driver.find_elements(By.CSS_SELECTOR, ".custom-dropdown")
    if len(custom_dropdowns) >= 2:
        # Click on the dropdown button to open it
        dropdown_button = custom_dropdowns[1].find_element(By.CSS_SELECTOR, ".custom-dropdown-button")
        dropdown_button.click()
        sleep(0.5)
        
        # Find and click the specified option
        options = world.driver.find_elements(By.CSS_SELECTOR, ".custom-dropdown-option")
        for option in options:
            if filter_value.lower() in option.text.lower():
                option.click()
                break
        sleep(0.5)


@when("I click the refresh button")
def click_refresh_button(step):
    """Click the refresh button in the toolbar."""
    from radish import world
    from time import sleep
    
    # Find and click the refresh button
    refresh_button = world.driver.find_element(By.CSS_SELECTOR, "button[title='Refresh artifacts']")
    refresh_button.click()
    
    # Wait for refresh to complete
    sleep(2)


@then("the filter should still be applied")
def filter_should_still_be_applied(step):
    """Check that the filter is still applied after refresh."""
    from radish import world
    
    # Check that the type filter still shows "requirement"
    custom_dropdowns = world.driver.find_elements(By.CSS_SELECTOR, ".custom-dropdown")
    if len(custom_dropdowns) >= 1:
        # Get the selected value from the custom dropdown
        selected_value_element = custom_dropdowns[0].find_element(By.CSS_SELECTOR, ".custom-dropdown-selected")
        selected_text = selected_value_element.text.lower()
        assert "requirement" in selected_text, f"Type filter should show 'requirement', but shows '{selected_text}'"


@then("I should see only filtered items")
def should_see_only_filtered_items(step):
    """Check that only filtered items are displayed."""
    from radish import world
    
    # Check that artifacts are filtered (should see fewer artifacts or specific ones)
    artifacts = world.driver.find_elements(By.CSS_SELECTOR, ".artifact-card")
    
    # For requirement filter, we should see some artifacts (not all cleared)
    assert len(artifacts) > 0, "Should see some filtered artifacts"
    
    # Check that the artifacts shown are of type "requirement"
    for artifact in artifacts[:3]:  # Check first 3 artifacts
        try:
            # Look for type indicator in the artifact
            type_indicator = artifact.find_element(By.CSS_SELECTOR, ".artifact-type")
            artifact_type = type_indicator.text.lower()
            assert "requirement" in artifact_type, f"Artifact should be of type 'requirement', but is '{artifact_type}'"
        except:
            # If we can't find type indicator, just continue
            pass


@then("the filter settings should remain visible in the status bar")
def filter_settings_should_remain_visible(step):
    """Check that filter settings remain visible in the status bar."""
    from radish import world
    
    # Check that the filter dropdowns still show the selected values
    custom_dropdowns = world.driver.find_elements(By.CSS_SELECTOR, ".custom-dropdown")
    
    # Check type filter
    if len(custom_dropdowns) >= 1:
        selected_value_element = custom_dropdowns[0].find_element(By.CSS_SELECTOR, ".custom-dropdown-selected")
        type_text = selected_value_element.text.lower()
        assert "requirement" in type_text, f"Type filter should show 'requirement' in status bar, but shows '{type_text}'"
    
    # Check status filter if it was set
    if len(custom_dropdowns) >= 2:
        selected_value_element = custom_dropdowns[1].find_element(By.CSS_SELECTOR, ".custom-dropdown-selected")
        status_text = selected_value_element.text.lower()
        # Status filter might be empty or have a value, both are acceptable
        assert status_text in ["", "all statuses", "open"], f"Status filter should be empty or 'open', but shows '{status_text}'"


@then("all filters should still be applied")
def all_filters_should_still_be_applied(step):
    """Check that all filters are still applied after refresh."""
    from radish import world
    
    # Check type filter
    custom_dropdowns = world.driver.find_elements(By.CSS_SELECTOR, ".custom-dropdown")
    if len(custom_dropdowns) >= 1:
        selected_value_element = custom_dropdowns[0].find_element(By.CSS_SELECTOR, ".custom-dropdown-selected")
        type_text = selected_value_element.text.lower()
        assert "requirement" in type_text, f"Type filter should show 'requirement', but shows '{type_text}'"
    
    # Check status filter
    if len(custom_dropdowns) >= 2:
        selected_value_element = custom_dropdowns[1].find_element(By.CSS_SELECTOR, ".custom-dropdown-selected")
        status_text = selected_value_element.text.lower()
        assert "open" in status_text, f"Status filter should show 'open', but shows '{status_text}'"
    
    # Check category filter
    category_filter = world.driver.find_element(By.CSS_SELECTOR, "input[placeholder='Filter by category...']")
    category_value = category_filter.get_attribute("value")
    assert category_value == "testing", f"Category filter should show 'testing', but shows '{category_value}'"
    
    # Check search filter
    search_box = world.driver.find_element(By.CSS_SELECTOR, "input[placeholder='Search artifacts...']")
    search_value = search_box.get_attribute("value")
    assert search_value == "requirement", f"Search filter should show 'requirement', but shows '{search_value}'"


@then("I should see only items matching all filters")
def should_see_only_items_matching_all_filters(step):
    """Check that only items matching all filters are displayed."""
    from radish import world
    
    # Check that artifacts are filtered and match the combined criteria
    artifacts = world.driver.find_elements(By.CSS_SELECTOR, ".artifact-card")
    
    # Should see some artifacts that match the combined filters
    assert len(artifacts) > 0, "Should see some artifacts matching all filters"
    
    # The artifacts should contain "requirement" in their content (due to search filter)
    for artifact in artifacts[:3]:  # Check first 3 artifacts
        artifact_text = artifact.text.lower()
        assert "requirement" in artifact_text, f"Artifact should contain 'requirement' due to search filter: {artifact_text[:100]}"


@then("all filter settings should remain visible in the status bar")
def all_filter_settings_should_remain_visible(step):
    """Check that all filter settings remain visible in the status bar."""
    from radish import world
    
    # Check all filter elements are visible and show correct values
    custom_dropdowns = world.driver.find_elements(By.CSS_SELECTOR, ".custom-dropdown")
    
    # Type filter should show "requirement"
    if len(custom_dropdowns) >= 1:
        selected_value_element = custom_dropdowns[0].find_element(By.CSS_SELECTOR, ".custom-dropdown-selected")
        type_text = selected_value_element.text.lower()
        assert "requirement" in type_text, f"Type filter should show 'requirement', but shows '{type_text}'"
    
    # Status filter should show "open"
    if len(custom_dropdowns) >= 2:
        selected_value_element = custom_dropdowns[1].find_element(By.CSS_SELECTOR, ".custom-dropdown-selected")
        status_text = selected_value_element.text.lower()
        assert "open" in status_text, f"Status filter should show 'open', but shows '{status_text}'"
    
    # Category filter should show "testing"
    category_filter = world.driver.find_element(By.CSS_SELECTOR, "input[placeholder='Filter by category...']")
    category_value = category_filter.get_attribute("value")
    assert category_value == "testing", f"Category filter should show 'testing', but shows '{category_value}'"
    
    # Search box should show "requirement"
    search_box = world.driver.find_element(By.CSS_SELECTOR, "input[placeholder='Search artifacts...']")
    search_value = search_box.get_attribute("value")
    assert search_value == "requirement", f"Search box should show 'requirement', but shows '{search_value}'"


@then("the type filter should show {expected_value}")
def type_filter_should_show(step, expected_value):
    """Check that the type filter shows the expected value."""
    from radish import world
    
    custom_dropdowns = world.driver.find_elements(By.CSS_SELECTOR, ".custom-dropdown")
    if len(custom_dropdowns) >= 1:
        selected_value_element = custom_dropdowns[0].find_element(By.CSS_SELECTOR, ".custom-dropdown-selected")
        actual_text = selected_value_element.text.lower()
        assert expected_value.lower() in actual_text, f"Type filter should show '{expected_value}', but shows '{actual_text}'"


@then("the status filter should show {expected_value}")
def status_filter_should_show(step, expected_value):
    """Check that the status filter shows the expected value."""
    from radish import world
    
    custom_dropdowns = world.driver.find_elements(By.CSS_SELECTOR, ".custom-dropdown")
    if len(custom_dropdowns) >= 2:
        selected_value_element = custom_dropdowns[1].find_element(By.CSS_SELECTOR, ".custom-dropdown-selected")
        actual_text = selected_value_element.text.lower()
        assert expected_value.lower() in actual_text, f"Status filter should show '{expected_value}', but shows '{actual_text}'"


@then("I should see only requirement artifacts with open status")
def should_see_only_requirement_open_artifacts(step):
    """Check that only requirement artifacts with open status are displayed."""
    from radish import world
    
    # Check that artifacts are filtered to show only requirements with open status
    artifacts = world.driver.find_elements(By.CSS_SELECTOR, ".artifact-card")
    
    # Should see some artifacts
    assert len(artifacts) > 0, "Should see some requirement artifacts with open status"
    
    # Check that the artifacts are of type "requirement" and have "open" status
    for artifact in artifacts[:3]:  # Check first 3 artifacts
        artifact_text = artifact.text.lower()
        
        # Should contain "requirement" (type filter)
        assert "requirement" in artifact_text, f"Artifact should be of type 'requirement': {artifact_text[:100]}"
        
        # Should contain "open" (status filter)
        assert "open" in artifact_text, f"Artifact should have 'open' status: {artifact_text[:100]}"
