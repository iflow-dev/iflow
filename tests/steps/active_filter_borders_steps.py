from radish import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Using existing step from simple_steps.py: "I am on the main page"


@given("the page has loaded completely")
def page_has_loaded_completely(world):
    """Wait for the page to load completely"""
    from radish import world
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    world.wait = WebDriverWait(world.driver, 10)
    # Wait for artifacts container to be present
    world.wait.until(EC.presence_of_element_located((By.ID, "artifacts-container")))
    # Wait for filters to be loaded
    world.wait.until(EC.presence_of_element_located((By.ID, "typeFilter")))
    world.wait.until(EC.presence_of_element_located((By.ID, "statusFilter")))


@when("I select a type filter {filter_value:QuotedString}")
def i_select_type_filter(step, filter_value):
    """Select a type filter value"""
    from radish import world
    
    # Use the JavaScript function to set the dropdown value
    result = world.driver.execute_script(f"return setDropdownValue('typeFilter', '{filter_value}');")
    
    if not result:
        raise AssertionError(f"Failed to set type filter to '{filter_value}'")
    
    # Wait for the filter to take effect
    import time
    time.sleep(1)


@when("I select a status filter {filter_value:QuotedString}")
def i_select_status_filter(step, filter_value):
    """Select a status filter value"""
    from radish import world
    
    # Use the JavaScript function to set the dropdown value
    result = world.driver.execute_script(f"return setDropdownValue('statusFilter', '{filter_value}');")
    
    if not result:
        raise AssertionError(f"Failed to set status filter to '{filter_value}'")
    
    # Wait for the filter to take effect
    import time
    time.sleep(1)


@when("I enter {text:QuotedString} in the category filter")
def i_enter_in_category_filter(step, text):
    """Enter text in the category filter"""
    from radish import world
    category_filter = world.driver.find_element(By.ID, "categoryFilter")
    category_filter.clear()
    category_filter.send_keys(text)


@when("I enter {text:QuotedString} in the search box")
def i_enter_in_search_box(step, text):
    """Enter text in the search box"""
    from radish import world
    search_input = world.driver.find_element(By.ID, "search-input")
    search_input.clear()
    search_input.send_keys(text)


@when("I clear the type filter")
def i_clear_type_filter(step):
    """Clear the type filter"""
    from radish import world
    
    # Use the JavaScript function to clear the dropdown value
    result = world.driver.execute_script("return setDropdownValue('typeFilter', '');")
    
    if not result:
        raise AssertionError("Failed to clear type filter")
    
    # Wait for the filter to take effect
    import time
    time.sleep(1)


@when("I clear the status filter")
def i_clear_status_filter(step):
    """Clear the status filter"""
    from radish import world
    
    # Use the JavaScript function to clear the dropdown value
    result = world.driver.execute_script("return setDropdownValue('statusFilter', '');")
    
    if not result:
        raise AssertionError("Failed to clear status filter")
    
    # Wait for the filter to take effect
    import time
    time.sleep(1)


@when("I clear the category filter")
def i_clear_category_filter(step):
    """Clear the category filter"""
    from radish import world
    
    # Use JavaScript to clear the category filter and update the state
    result = world.driver.execute_script("return clearCategoryFilter();")
    
    # Wait for the filter to take effect
    import time
    time.sleep(1)


@when("I clear the search input")
def i_clear_search_input(step):
    """Clear the search input"""
    from radish import world
    
    # Use JavaScript to clear the search input and update the state
    result = world.driver.execute_script("return clearSearchFilter();")
    
    # Wait for the filter to take effect
    import time
    time.sleep(1)


@when("I clear all filters")
def i_clear_all_filters(step):
    """Clear all filters"""
    i_clear_type_filter(step)
    i_clear_status_filter(step)
    i_clear_category_filter(step)
    i_clear_search_input(step)


@then("the type filter should have an orange border")
def type_filter_should_have_orange_border(step):
    """Verify the type filter has an orange border"""
    from radish import world
    type_filter = world.driver.find_element(By.ID, "typeFilter")
    assert "active" in type_filter.get_attribute("class"), "Type filter should have 'active' class for orange border"


@then("the status filter should have an orange border")
def status_filter_should_have_orange_border(step):
    """Verify the status filter has an orange border"""
    from radish import world
    status_filter = world.driver.find_element(By.ID, "statusFilter")
    assert "active" in status_filter.get_attribute("class"), "Status filter should have 'active' class for orange border"


@then("the category filter should have an orange border")
def category_filter_should_have_orange_border(step):
    """Verify the category filter has an orange border"""
    from radish import world
    category_filter = world.driver.find_element(By.ID, "categoryFilter")
    assert "active" in category_filter.get_attribute("class"), "Category filter should have 'active' class for orange border"


@then("the search input should have an orange border")
def search_input_should_have_orange_border(step):
    """Verify the search input has an orange border"""
    from radish import world
    search_input = world.driver.find_element(By.ID, "search-input")
    assert "active" in search_input.get_attribute("class"), "Search input should have 'active' class for orange border"


@then("the type filter should not have an orange border")
def type_filter_should_not_have_orange_border(step):
    """Verify the type filter does not have an orange border"""
    from radish import world
    type_filter = world.driver.find_element(By.ID, "typeFilter")
    assert "active" not in type_filter.get_attribute("class"), "Type filter should not have 'active' class"


@then("the status filter should not have an orange border")
def status_filter_should_not_have_orange_border(step):
    """Verify the status filter does not have an orange border"""
    from radish import world
    status_filter = world.driver.find_element(By.ID, "statusFilter")
    assert "active" not in status_filter.get_attribute("class"), "Status filter should not have 'active' class"


@then("the category filter should not have an orange border")
def category_filter_should_not_have_orange_border(step):
    """Verify the category filter does not have an orange border"""
    from radish import world
    category_filter = world.driver.find_element(By.ID, "categoryFilter")
    assert "active" not in category_filter.get_attribute("class"), "Category filter should not have 'active' class"


@then("the search input should not have an orange border")
def search_input_should_not_have_orange_border(step):
    """Verify the search input does not have an orange border"""
    from radish import world
    search_input = world.driver.find_element(By.ID, "search-input")
    assert "active" not in search_input.get_attribute("class"), "Search input should not have 'active' class"


@then("no filters should have orange borders")
def no_filters_should_have_orange_borders(step):
    """Verify no filters have orange borders"""
    from radish import world
    type_filter = world.driver.find_element(By.ID, "typeFilter")
    status_filter = world.driver.find_element(By.ID, "statusFilter")
    category_filter = world.driver.find_element(By.ID, "categoryFilter")
    search_input = world.driver.find_element(By.ID, "search-input")
    
    assert "active" not in type_filter.get_attribute("class"), "Type filter should not have 'active' class"
    assert "active" not in status_filter.get_attribute("class"), "Status filter should not have 'active' class"
    assert "active" not in category_filter.get_attribute("class"), "Category filter should not have 'active' class"
    assert "active" not in search_input.get_attribute("class"), "Search input should not have 'active' class"
