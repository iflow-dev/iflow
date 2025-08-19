"""
Editor control class for BDD test automation.
This module provides controls for managing artifact creation and editing in the modal.
"""

import sys
import os
# Add the tests directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from controls.base import ControlBase
from controls.input_field import InputField
from controls.button import Button


class Editor(ControlBase):
    """Control for managing artifact creation and editing in the modal."""
    
    def __init__(self, driver):
        """Initialize the artifact editor control."""
        # The editor operates within the artifact modal
        super().__init__("//div[@id='artifactModal']")
        
        # Store the driver for internal use
        self.driver = driver
        
        # Initialize field controls
        self.summary_field = InputField("summary")
        self.description_field = InputField("description")
        self.category_field = InputField("category")
        self.status_field = InputField("status")
        self.type_field = InputField("type")
        
        # Button controls
        self.create_button = Button("Create", context="modal")
        self.cancel_button = Button("Cancel", context="modal")
    
    def open(self):
        """Open the artifact creation modal."""
        from controls.button import Button
        create_button = Button("Create", context="toolbar")
        create_button.click(self.driver)
        
        # Wait for modal to be visible using locate()
        self.locate(self.driver)
        
        # Wait for JavaScript to populate dropdown options
        import time
        time.sleep(3)
        
        return self
    
    def close(self):
        """Close the artifact creation modal."""
        from controls.button import Button
        close_button = Button("×", context="modal")
        try:
            close_button.click(self.driver)
        except:
            # If close button not found, try cancel button
            self.cancel_button.click(self.driver)
    
    def set_summary(self, summary):
        """Set the artifact summary."""
        return self.summary_field.set_value(self.driver, summary)
    
    def set_description(self, description):
        """Set the artifact description."""
        return self.description_field.set_value(self.driver, description)
    
    def set_category(self, category):
        """Set the artifact category."""
        return self.category_field.set_value(self.driver, category)
    
    def set_status(self, status):
        """Set the artifact status."""
        return self.status_field.set_value(self.driver, status)
    
    def set_type(self, artifact_type):
        """Set the artifact type."""
        return self.type_field.set_value(self.driver, artifact_type)
    
    def get_summary(self):
        """Get the current artifact summary."""
        return self.summary_field.get_value(self.driver)
    
    def get_description(self):
        """Get the current artifact description."""
        return self.description_field.get_value(self.driver)
    
    def get_category(self):
        """Get the current artifact category."""
        return self.category_field.get_value(self.driver)
    
    def get_status(self):
        """Get the current artifact status."""
        return self.status_field.get_value(self.driver)
    
    def get_type(self):
        """Get the current artifact type."""
        return self.type_field.get_value(self.driver)
    
    def create(self):
        """Create the artifact and close the modal."""
        self.create_button.click(self.driver)
        
        # Wait for modal to close (modal should disappear)
        try:
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.common.by import By
            
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.invisibility_of_element_located((By.ID, "artifactModal")))
        except:
            # If modal doesn't close automatically, force close it
            self.close()
        
        return True
    
    def cancel(self):
        """Cancel artifact creation and close the modal."""
        self.cancel_button.click(self.driver)
        
        # Wait for modal to close
        try:
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.common.by import By
            
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.invisibility_of_element_located((By.ID, "artifactModal")))
        except:
            # If modal doesn't close automatically, force close it
            self.close()
        
        return True
    
    def abort(self):
        """Abort artifact creation (same as cancel)."""
        return self.cancel()
    
    def is_open(self):
        """Check if the editor modal is currently open."""
        try:
            from selenium.webdriver.common.by import By
            modal = self.driver.find_element(By.ID, "artifactModal")
            return modal.is_displayed()
        except:
            return False
    
    def is_closed(self):
        """Check if the editor modal is currently closed."""
        return not self.is_open()
    
    def wait_for_visible(self, timeout=5):
        """Wait for the editor modal to become visible."""
        # Use the existing locate method which already handles waiting
        self.locate(self.driver, timeout)
        return True
