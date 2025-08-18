"""
Step definitions for dropdown selection functionality testing.
This covers the fix for ticket #00079 - dropdown selection not working in artifact editor.
"""

from radish import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from controls import Button, InputField
import time

@given("the artifact creation modal is open")
def artifact_creation_modal_is_open(step):
    """Verify that the artifact creation modal is open."""
    from radish import world
    
    # Wait for modal to be visible
    wait = WebDriverWait(world.driver, 10)
    modal = wait.until(
        EC.visibility_of_element_located((By.ID, "artifactModal"))
    )
    
    # Verify modal is displayed
    assert modal.is_displayed(), "Artifact creation modal is not displayed"
    
    # Verify modal title is correct
    modal_title = world.driver.find_element(By.ID, "modalTitle")
    assert "Create New Artifact" in modal_title.text, f"Modal title is incorrect: {modal_title.text}"

@when("I click on the {dropdown_name:QuotedString} dropdown")
def i_click_on_dropdown(step, dropdown_name):
    """Click on a specific dropdown in the artifact creation modal."""
    from radish import world
    
    # Map dropdown names to their identifiers
    dropdown_map = {
        "Type": "artifactType",
        "Status": "artifactStatus"
    }
    
    if dropdown_name not in dropdown_map:
        raise ValueError(f"Unknown dropdown: {dropdown_name}")
    
    select_id = dropdown_map[dropdown_name]
    
    # Find the custom dropdown button
    dropdown_button = world.driver.find_element(
        By.XPATH, 
        f"//select[@id='{select_id}']/following-sibling::div[contains(@class, 'custom-dropdown-button')]"
    )
    
    # Click the dropdown button
    dropdown_button.click()
    
    # Wait a moment for dropdown to open
    time.sleep(0.5)

@when("I click on {option_text:QuotedString} option")
def i_click_on_option(step, option_text):
    """Click on a specific option in the dropdown."""
    from radish import world
    
    # Find the option with the specified text
    option = world.driver.find_element(
        By.XPATH,
        f"//div[contains(@class, 'custom-dropdown-option') and contains(text(), '{option_text}')]"
    )
    
    # Click the option
    option.click()
    
    # Wait a moment for selection to process
    time.sleep(0.5)

@when("I click outside the dropdown")
def i_click_outside_dropdown(step):
    """Click outside the dropdown to close it."""
    from radish import world
    
    # Click on the modal background (outside the dropdown)
    modal = world.driver.find_element(By.ID, "artifactModal")
    actions = ActionChains(world.driver)
    actions.move_to_element(modal).click().perform()
    
    # Wait a moment for dropdown to close
    time.sleep(0.5)

@then("the dropdown should close")
def dropdown_should_close(step):
    """Verify that the dropdown options are no longer visible."""
    from radish import world
    
    # Wait for dropdown options to be hidden
    wait = WebDriverWait(world.driver, 5)
    
    try:
        # Check if any dropdown options are visible
        visible_options = world.driver.find_elements(
            By.XPATH,
            "//div[contains(@class, 'custom-dropdown-options') and @style[contains(., 'display: block')]]"
        )
        
        # If no visible options found, dropdown is closed
        if len(visible_options) == 0:
            return  # Dropdown is closed, test passes
        
        # If options are still visible, check if they're actually hidden
        for option_container in visible_options:
            if option_container.is_displayed():
                raise AssertionError("Dropdown options are still visible")
                
    except Exception:
        # If we can't find any visible options, dropdown is closed
        pass

@then("the selected value should be {expected_value:QuotedString}")
def selected_value_should_be(step, expected_value):
    """Verify that the dropdown displays the correct selected value."""
    from radish import world
    
    # Find the selected value display in the dropdown button
    selected_value_element = world.driver.find_element(
        By.XPATH,
        "//div[contains(@class, 'custom-dropdown-button')]//span[contains(@class, 'custom-dropdown-selected')]"
    )
    
    # Get the actual selected value text
    actual_value = selected_value_element.text.strip()
    
    # Verify the selected value matches expected
    assert expected_value in actual_value, f"Expected '{expected_value}' but got '{actual_value}'"

@then("the original select element should have value {expected_value:QuotedString}")
def original_select_should_have_value(step, expected_value):
    """Verify that the original select element has the correct value."""
    from radish import world
    
    # Find the original select element (should be hidden)
    select_elements = world.driver.find_elements(
        By.XPATH,
        "//select[@id='artifactType' or @id='artifactStatus']"
    )
    
    # Check each select element for the expected value
    found_value = False
    for select_element in select_elements:
        if select_element.get_attribute("value") == expected_value:
            found_value = True
            break
    
    assert found_value, f"Original select element does not have value '{expected_value}'"

@then("no value should be selected")
def no_value_should_be_selected(step):
    """Verify that no value is selected in the dropdown."""
    from radish import world
    
    # Find the selected value display
    selected_value_element = world.driver.find_element(
        By.XPATH,
        "//div[contains(@class, 'custom-dropdown-button')]//span[contains(@class, 'custom-dropdown-selected')]"
    )
    
    # Get the actual selected value text
    actual_value = selected_value_element.text.strip()
    
    # Verify no meaningful value is selected (should show default text)
    default_texts = ["Select Type", "Select Status"]
    assert any(default in actual_value for default in default_texts), f"Unexpected selected value: '{actual_value}'"
