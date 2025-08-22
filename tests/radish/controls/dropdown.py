"""
Dropdown control class for BDD test automation.
This module provides controls for custom dropdown elements.
"""

import sys
import os
# Add the tests directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from controls.base import ControlBase


class Dropdown(ControlBase):
    """Control for custom dropdown elements."""
    
    def __init__(self, dropdown_type):
        """
        Initialize dropdown control.
        
        Args:
            dropdown_type: Either 'type' or 'status' to identify which dropdown
        """
        if dropdown_type == 'type':
            # First custom dropdown (type filter)
            super().__init__("(//div[contains(@class, 'custom-dropdown')])[1]")
        elif dropdown_type == 'status':
            # Second custom dropdown (status filter)
            super().__init__("(//div[contains(@class, 'custom-dropdown')])[2]")
        else:
            raise ValueError(f"Unknown dropdown type: {dropdown_type}")
        
        self.dropdown_type = dropdown_type
    
    def get_selected_value(self, timeout=None):
        """Get the currently selected value from the dropdown."""
        dropdown = self.locate(timeout)
        selected_element = dropdown.find_element("xpath", ".//div[contains(@class, 'custom-dropdown-selected')]")
        return selected_element.text
    
    def select_option(self, option_text, timeout=None):
        """Select an option from the dropdown by text."""
        # Click to open dropdown
        dropdown = self.locate(timeout)
        
        # Try different approaches to find the button
        try:
            # First try: direct child with class
            button = dropdown.find_element("xpath", ".//div[contains(@class, 'custom-dropdown-button')]")
        except:
            try:
                # Second try: any descendant with class
                button = dropdown.find_element("xpath", ".//*[contains(@class, 'custom-dropdown-button')]")
            except:
                # Third try: first div child (fallback)
                button = dropdown.find_element("xpath", ".//div[1]")
        
        button.click()
        
        # Wait a moment for dropdown to open
        import time
        time.sleep(0.5)
        
        # Find and click the option
        options = dropdown.find_elements("xpath", ".//div[contains(@class, 'custom-dropdown-option')]")
        for option in options:
            option_text_lower = option_text.lower()
            option_text_content = option.text.lower()
            
            # Check if the option text contains the target text
            if option_text_lower in option_text_content:
                option.click()
                return
        
        raise ValueError(f"Option '{option_text}' not found in {self.dropdown_type} dropdown")
    
    def is_open(self, timeout=None):
        """Check if the dropdown is currently open."""
        try:
            dropdown = self.locate(timeout)
            options_container = dropdown.find_element("xpath", ".//div[contains(@class, 'custom-dropdown-options')]")
            return options_container.is_displayed()
        except:
            return False
