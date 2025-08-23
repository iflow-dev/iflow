"""
Dropdown control classes for BDD test automation.
This module provides controls for both native select dropdowns and custom div dropdowns.
"""

from abc import ABC, abstractmethod
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import logging

# Set up logging
log = logging.getLogger(__name__)


class BaseDropdown(ABC):
    """Abstract base class for dropdown controls."""
    
    def __init__(self, element):
        """Initialize with a dropdown element."""
        self.element = element
    
    @abstractmethod
    def set_value(self, value):
        """Set the dropdown value."""
        pass
    
    @abstractmethod
    def get_value(self):
        """Get the current dropdown value."""
        pass
    
    @abstractmethod
    def get_options(self):
        """Get available dropdown options."""
        pass


class SelectDropdown(BaseDropdown):
    """Control for native HTML select dropdowns."""
    
    def __init__(self, element):
        """Initialize with a select element."""
        super().__init__(element)
        self.select = Select(element)
    
    def set_value(self, value):
        """Set the dropdown value using native select methods."""
        try:
            log.trace(f"Setting native select dropdown to value '{value}'")
            self.select.select_by_value(value)
            log.trace(f"Successfully set native select dropdown to '{value}'")
        except Exception as e:
            log.error(f"Failed to set native select dropdown to '{value}': {e}")
            raise
    
    def get_value(self):
        """Get the current selected value."""
        try:
            selected_option = self.select.first_selected_option
            return selected_option.get_attribute("value")
        except Exception as e:
            log.error(f"Failed to get native select dropdown value: {e}")
            return None
    
    def get_options(self):
        """Get all available options."""
        try:
            return [option.get_attribute("value") for option in self.select.options]
        except Exception as e:
            log.error(f"Failed to get native select dropdown options: {e}")
            return []


class CustomDropdown(BaseDropdown):
    """Control for custom div-based dropdowns."""
    
    def __init__(self, element):
        """Initialize with a custom dropdown div element."""
        super().__init__(element)
    
    def set_value(self, value):
        """Set the dropdown value using JavaScript."""
        try:
            log.trace(f"Setting custom dropdown to value '{value}'")
            # Find the input field within the custom dropdown
            input_field = self.element.find_element(By.CSS_SELECTOR, "input[data-field]")
            
            # Set the value using JavaScript
            self.element.parent.execute_script(
                f"arguments[0].value = '{value}'; "
                f"arguments[0].dispatchEvent(new Event('change'));", 
                input_field
            )
            
            # Trigger a click on the dropdown to ensure it's properly activated
            self.element.click()
            
            log.trace(f"Successfully set custom dropdown to '{value}'")
        except Exception as e:
            log.error(f"Failed to set custom dropdown to '{value}': {e}")
            raise
    
    def get_value(self):
        """Get the current value from the custom dropdown."""
        try:
            input_field = self.element.find_element(By.CSS_SELECTOR, "input[data-field]")
            return input_field.get_attribute("value")
        except Exception as e:
            log.error(f"Failed to get custom dropdown value: {e}")
            return None
    
    def get_options(self):
        """Get available options from the custom dropdown."""
        try:
            # Custom dropdowns might store options in data attributes or child elements
            # This is a simplified implementation
            return []
        except Exception as e:
            log.error(f"Failed to get custom dropdown options: {e}")
            return []


class DropdownFactory:
    """Factory class to create appropriate dropdown controls."""
    
    @staticmethod
    def create_dropdown(driver, element_id, timeout=10):
        """
        Create a dropdown control for the given element ID.
        
        Args:
            driver: WebDriver instance
            element_id: ID of the dropdown element
            timeout: Timeout for element location
            
        Returns:
            BaseDropdown instance (SelectDropdown or CustomDropdown)
        """
        wait = WebDriverWait(driver, timeout)
        
        try:
            # First try to find a native select element
            select_element = wait.until(EC.element_to_be_clickable((By.ID, element_id)))
            if select_element.tag_name.lower() == "select":
                log.trace(f"Found native select dropdown for '{element_id}'")
                return SelectDropdown(select_element)
        except TimeoutException:
            log.trace(f"Native select not found for '{element_id}', looking for custom dropdown")
        
        try:
            # Look for custom dropdown div
            custom_dropdown_xpath = f"//div[@class='custom-dropdown' and .//input[@data-field='{element_id}']]"
            custom_element = wait.until(EC.element_to_be_clickable((By.XPATH, custom_dropdown_xpath)))
            log.trace(f"Found custom dropdown for '{element_id}'")
            return CustomDropdown(custom_element)
        except TimeoutException:
            log.trace(f"Custom dropdown not found for '{element_id}', trying fallback")
        
        try:
            # Fallback: try to find any element with the ID
            fallback_element = wait.until(EC.presence_of_element_located((By.ID, element_id)))
            log.trace(f"Found fallback element for '{element_id}'")
            
            # Determine type based on tag name
            if fallback_element.tag_name.lower() == "select":
                return SelectDropdown(fallback_element)
            else:
                return CustomDropdown(fallback_element)
        except TimeoutException:
            raise TimeoutException(f"Could not find dropdown element with ID '{element_id}' after {timeout} seconds")
