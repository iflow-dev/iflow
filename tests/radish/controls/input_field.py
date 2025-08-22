"""
Input field control for BDD test automation.
This module provides controls for input fields and form elements.
"""

import sys
import os
# Add the tests directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from controls.base import ControlBase
from selenium.webdriver.common.by import By


class InputField(ControlBase):
    """Control for locating and interacting with input fields."""
    
    def __init__(self, field_type):
        """
        Initialize input field control.
        
        Args:
            field_type: Type of input field (e.g., "summary", "description", "status")
        """
        if field_type == "summary":
            xpath = "//input[@id='artifactSummary']"
        elif field_type == "description":
            xpath = "//textarea[@id='artifactDescription']"
        elif field_type == "category":
            xpath = "//input[@id='artifactCategory']"
        elif field_type == "status":
            xpath = "//select[@id='artifactStatus']"
        elif field_type == "type":
            xpath = "//select[@id='artifactType']"
        else:
            xpath = f"//input[@name='{field_type}' or @id='{field_type}' or @placeholder='{field_type}']"
        super().__init__(xpath)
    
    def set_value(self, driver, value, timeout=5):
        """Set the value of the input field."""
        element = self.locate(driver, timeout)
        
        # Handle different element types
        tag_name = element.tag_name.lower()
        if tag_name == 'select':
            # Check if this is a custom dropdown (div-based) or standard select
            try:
                # Look for custom dropdown structure
                custom_dropdown = element.find_element(By.XPATH, "..//div[contains(@class, 'custom-dropdown')]")
                if custom_dropdown:
                    print(f"Found custom dropdown, using custom dropdown method for '{value}'")
                    return self._set_custom_dropdown_value(driver, custom_dropdown, value)
            except:
                pass
            
            # Fall back to standard select handling
            return self._set_standard_select_value(driver, element, value)
        else:
            # For input/textarea elements, clear and send keys
            element.clear()
            element.send_keys(value)
        
        return element
    
    def _set_custom_dropdown_value(self, driver, dropdown_element, value):
        """Set value for custom dropdown (div-based) using JavaScript accessibility functions."""
        from selenium.webdriver.common.by import By
        import time
        
        try:
            # Get the original select element ID
            original_select = None
            try:
                # Look for the original select element in the same parent
                parent = dropdown_element.find_element(By.XPATH, "..")
                original_select = parent.find_element(By.TAG_NAME, "select")
                select_id = original_select.get_attribute("id")
                print(f"Found original select element: {select_id}")
            except Exception as e:
                print(f"Could not find original select element: {e}")
                return dropdown_element
            
            # Use the new JavaScript accessibility function to set the value
            print(f"Using JavaScript accessibility function to set dropdown value '{value}'...")
            
            # Call the global setDropdownValue function
            result = driver.execute_script(f"""
                if (typeof setDropdownValue === 'function') {{
                    return setDropdownValue('{select_id}', '{value}');
                }} else {{
                    console.error('setDropdownValue function not available');
                    return false;
                }}
            """)
            
            if result:
                print(f"Successfully set dropdown value '{value}' using JavaScript accessibility function")
                
                # Verify the value was set correctly
                actual_value = driver.execute_script(f"""
                    if (typeof getDropdownValue === 'function') {{
                        return getDropdownValue('{select_id}');
                    }} else {{
                        return null;
                    }}
                """)
                
                if actual_value == value:
                    print(f"Verified dropdown value is now '{actual_value}'")
                else:
                    print(f"Warning: Expected value '{value}', but got '{actual_value}'")
                
                return dropdown_element
            else:
                print(f"Failed to set dropdown value '{value}' using JavaScript accessibility function")
                raise Exception(f"JavaScript setDropdownValue returned false for value '{value}'")
                
        except Exception as e:
            print(f"JavaScript accessibility function failed: {e}")
            raise Exception(f"Failed to set dropdown value '{value}' using accessibility functions: {e}")
    
    def _set_standard_select_value(self, driver, element, value):
        """Set value for standard HTML select element."""
        import time
        from selenium.webdriver.common.by import By
        
        # Wait for dropdown options to be populated
        max_wait = 10  # Wait up to 10 seconds
        wait_time = 0
        while wait_time < max_wait:
            try:
                # Check if there are any options with values (not just the default "Select Type" option)
                options = element.find_elements(By.CSS_SELECTOR, 'option[value]')
                if len(options) > 1:  # More than just the default option
                    print(f"Dropdown options populated after {wait_time}s, found {len(options)} options")
                    break
                time.sleep(0.5)
                wait_time += 0.5
            except Exception as e:
                print(f"Error checking dropdown options: {e}")
                time.sleep(0.5)
                wait_time += 0.5
        
        if wait_time >= max_wait:
            print("Warning: Dropdown options not populated after waiting")
        
        # Now try to select the value using multiple methods
        success = False
        
        # Method 1: Try Select class
        if not success:
            try:
                from selenium.webdriver.support.ui import Select
                select = Select(element)
                select.select_by_value(value)
                print(f"Successfully selected '{value}' using Select class")
                success = True
            except Exception as e:
                print(f"Select class method failed: {e}")
        
        # Method 2: Try JavaScript
        if not success:
            try:
                driver.execute_script(f"arguments[0].value = '{value}';", element)
                print(f"Successfully selected '{value}' using JavaScript")
                success = True
            except Exception as e:
                print(f"JavaScript method failed: {e}")
        
        # Method 3: Try clicking the option directly
        if not success:
            try:
                option = element.find_element(By.CSS_SELECTOR, f'option[value="{value}"]')
                option.click()
                print(f"Successfully selected '{value}' using click method")
                success = True
            except Exception as e:
                print(f"Click method failed: {e}")
        
        if not success:
            raise Exception(f"All methods failed to select '{value}' from dropdown")
        
        return element
    
    def get_value(self, driver, timeout=5):
        """Get the current value of the input field."""
        element = self.locate(driver, timeout)
        return element.get_attribute("value")
