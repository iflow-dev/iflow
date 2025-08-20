from radish import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@when("I toggle the flag filter")
def i_toggle_flag_filter(step):
    """Toggle the flag filter on/off"""
    from radish import world
    flag_filter = world.driver.find_element(By.ID, "flagFilter")
    flag_filter.click()
    
    # Wait for the filter to take effect
    import time
    time.sleep(1)


@when("I click the clear all button")
def i_click_clear_all_button(step):
    """Click the clear all filters button"""
    from radish import world
    clear_all_btn = world.driver.find_element(By.ID, "clearAllFilters")
    clear_all_btn.click()
    
    # Wait for the filters to be cleared
    import time
    time.sleep(1)


@when("I click the search clear button")
def i_click_search_clear_button(step):
    """Click the search clear button"""
    from radish import world
    clear_search_btn = world.driver.find_element(By.ID, "clearSearch")
    clear_search_btn.click()
    
    # Wait for the search to be cleared
    import time
    time.sleep(1)


@when("I click the category clear button")
def i_click_category_clear_button(step):
    """Click the category clear button"""
    from radish import world
    clear_category_btn = world.driver.find_element(By.ID, "clearCategory")
    clear_category_btn.click()
    
    # Wait for the category filter to be cleared
    import time
    time.sleep(1)


@then("the search clear button should be visible")
def search_clear_button_should_be_visible(step):
    """Verify the search clear button is visible"""
    from radish import world
    clear_search_btn = world.driver.find_element(By.ID, "clearSearch")
    assert "visible" in clear_search_btn.get_attribute("class"), "Search clear button should be visible"


@then("the category clear button should be visible")
def category_clear_button_should_be_visible(step):
    """Verify the category clear button is visible"""
    from radish import world
    clear_category_btn = world.driver.find_element(By.ID, "clearCategory")
    assert "visible" in clear_category_btn.get_attribute("class"), "Category clear button should be visible"


@then("the search clear button should not be visible")
def search_clear_button_should_not_be_visible(step):
    """Verify the search clear button is not visible"""
    from radish import world
    clear_search_btn = world.driver.find_element(By.ID, "clearSearch")
    assert "visible" not in clear_search_btn.get_attribute("class"), "Search clear button should not be visible"


@then("the category clear button should not be visible")
def category_clear_button_should_not_be_visible(step):
    """Verify the category clear button is not visible"""
    from radish import world
    clear_category_btn = world.driver.find_element(By.ID, "clearCategory")
    assert "visible" not in clear_category_btn.get_attribute("class"), "Category clear button should not be visible"


@then("the clear all button should be enabled")
def clear_all_button_should_be_enabled(step):
    """Verify the clear all button is enabled"""
    from radish import world
    clear_all_btn = world.driver.find_element(By.ID, "clearAllFilters")
    assert not clear_all_btn.get_attribute("disabled"), "Clear all button should be enabled"


@then("the clear all button should be disabled")
def clear_all_button_should_be_disabled(step):
    """Verify the clear all button is disabled"""
    from radish import world
    clear_all_btn = world.driver.find_element(By.ID, "clearAllFilters")
    assert clear_all_btn.get_attribute("disabled"), "Clear all button should be disabled"


@then("all filters should have active states")
def all_filters_should_have_active_states(step):
    """Verify all filters have active states"""
    from radish import world
    
    # Check type filter
    type_filter = world.driver.find_element(By.ID, "typeFilter")
    assert "active" in type_filter.get_attribute("class"), "Type filter should have active state"
    
    # Check status filter
    status_filter = world.driver.find_element(By.ID, "statusFilter")
    assert "active" in status_filter.get_attribute("class"), "Status filter should have active state"
    
    # Check search input
    search_input = world.driver.find_element(By.ID, "search-input")
    assert "active" in search_input.get_attribute("class"), "Search input should have active state"
    
    # Check category filter
    category_filter = world.driver.find_element(By.ID, "categoryFilter")
    assert "active" in category_filter.get_attribute("class"), "Category filter should have active state"
    
    # Check flag filter
    flag_filter = world.driver.find_element(By.ID, "flagFilter")
    assert "active" in flag_filter.get_attribute("class"), "Flag filter should have active state"


@then("no filters should have active states")
def no_filters_should_have_active_states(step):
    """Verify no filters have active states"""
    from radish import world
    
    # Check type filter
    type_filter = world.driver.find_element(By.ID, "typeFilter")
    assert "active" not in type_filter.get_attribute("class"), "Type filter should not have active state"
    
    # Check status filter
    status_filter = world.driver.find_element(By.ID, "statusFilter")
    assert "active" not in status_filter.get_attribute("class"), "Status filter should not have active state"
    
    # Check search input
    search_input = world.driver.find_element(By.ID, "search-input")
    assert "active" not in search_input.get_attribute("class"), "Search input should not have active state"
    
    # Check category filter
    category_filter = world.driver.find_element(By.ID, "categoryFilter")
    assert "active" not in category_filter.get_attribute("class"), "Category filter should not have active state"
    
    # Check flag filter
    flag_filter = world.driver.find_element(By.ID, "flagFilter")
    assert "active" not in flag_filter.get_attribute("class"), "Flag filter should not have active state"


@then("both clear buttons should be visible")
def both_clear_buttons_should_be_visible(step):
    """Verify both clear buttons are visible"""
    from radish import world
    
    clear_search_btn = world.driver.find_element(By.ID, "clearSearch")
    clear_category_btn = world.driver.find_element(By.ID, "clearCategory")
    
    assert "visible" in clear_search_btn.get_attribute("class"), "Search clear button should be visible"
    assert "visible" in clear_category_btn.get_attribute("class"), "Category clear button should be visible"


@then("the search input should be cleared")
def search_input_should_be_cleared(step):
    """Verify the search input is cleared"""
    from radish import world
    search_input = world.driver.find_element(By.ID, "search-input")
    assert search_input.get_attribute("value") == "", "Search input should be cleared"


@then("the category filter should be cleared")
def category_filter_should_be_cleared(step):
    """Verify the category filter is cleared"""
    from radish import world
    category_filter = world.driver.find_element(By.ID, "categoryFilter")
    assert category_filter.get_attribute("value") == "", "Category filter should be cleared"


@then("the category clear button should still be visible")
def category_clear_button_should_still_be_visible(step):
    """Verify the category clear button is still visible"""
    from radish import world
    clear_category_btn = world.driver.find_element(By.ID, "clearCategory")
    assert "visible" in clear_category_btn.get_attribute("class"), "Category clear button should still be visible"
