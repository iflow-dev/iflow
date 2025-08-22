"""
Editor control class for BDD test automation.
This module provides controls for managing artifact creation and editing in the modal.
"""

import sys
import os
import logging
import time
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


from controls.base import ControlBase
from controls.input_field import InputField
from controls.button import Button
from controls.page import Page
from controls.toolbar import Toolbar

# Set up logging
log = logging.getLogger(__name__)


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
        
        # Flag control
        from controls.flag import Flag
        self.flag = Flag(driver)
        
        # Button controls
        self.submit_button = Button("submit", None, None)  # Will find any submit button regardless of text
        self.cancel_button = Button("button", "Cancel", None)  # Button with text "Cancel"
    
    def open(self):
        """Open the artifact creation modal."""
        log.trace("Waiting for toolbar to be fully loaded...")
        
        # Wait for the toolbar to be fully loaded (not just the loading message)
        page = Page()
        page.wait()

        # Use Toolbar pattern to access create button
        toolbar = Toolbar(self.driver)
        
        # Use the new Toolbar().buttons.create pattern
        log.trace("Clicking create button via Toolbar().buttons.create...")
        toolbar.buttons.create.click()
        
        # Wait for modal to be visible using locate()
        self.locate()
        
        # Wait for JavaScript to populate dropdown options
        time.sleep(3)
        
        return self
    
    def close(self):
        """Close the artifact creation modal."""
        

        # no autodiscovery
        # Try to find the close button (×) in the modal
        close_button = Button("text", "×", None)
        try:
            close_button.click()
        except:
            # If close button not found, try cancel button
            self.cancel_button.click()
    
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
    
    def set(self, field, value):
        """Generic method to set any artifact field to a specified value."""
        log = logging.getLogger(__name__)
        log.trace(f"Setting field '{field}' to value '{value}'")
        
        try:
            # Map field names to element IDs and handling methods
            field_mapping = {
                "type": ("artifactType", "select"),
                "summary": ("artifactSummary", "input"),
                "description": ("artifactDescription", "textarea"),
                "category": ("artifactCategory", "input"),
                "status": ("artifactStatus", "select"),
                "verification": ("artifactVerification", "input"),
                "activity": ("artifactActivity", "input"),
                "iteration": ("artifactIteration", "input"),
                "flagged": ("artifactFlagged", "checkbox")
            }
            
            if field.lower() not in field_mapping:
                raise ValueError(f"Unknown field '{field}'. Supported fields: {', '.join(field_mapping.keys())}")
            
            element_id, field_type = field_mapping[field.lower()]
            
            # Wait for the element to be present
            wait = WebDriverWait(self.driver, 10)
            element = wait.until(EC.presence_of_element_located((By.ID, element_id)))
            
            if field_type == "select":
                # Handle dropdown/select fields
                select = Select(element)
                select.select_by_value(value)
                log.trace(f"Set select field '{field}' to '{value}'")
            elif field_type == "input":
                # Handle text input fields
                element.clear()
                element.send_keys(value)
                log.trace(f"Set input field '{field}' to '{value}'")
            elif field_type == "textarea":
                # Handle textarea fields
                element.clear()
                element.send_keys(value)
                log.trace(f"Set textarea field '{field}' to '{value}'")
            elif field_type == "checkbox":
                # Handle checkbox fields
                if value.lower() in ["true", "yes", "1", "checked"]:
                    if not element.is_selected():
                        element.click()
                    log.trace(f"Checked checkbox field '{field}'")
                else:
                    if element.is_selected():
                        element.click()
                    log.trace(f"Unchecked checkbox field '{field}'")
            
        except Exception as e:
            log.error(f"Failed to set field '{field}' to '{value}': {e}")
            raise AssertionError(f"Failed to set field '{field}' to '{value}': {e}")
    
    def create(self):
        """Create the artifact and close the modal."""
        self.submit_button.click()
        
        # Wait for modal to close (modal should disappear)
        try:
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.invisibility_of_element_located((By.ID, "artifactModal")))
        except Exception as e:
            # If modal doesn't close automatically, show full error and force close it
            print(f"Modal did not close automatically. Full error: {str(e)}")
            print(f"Exception type: {type(e).__name__}")
            import traceback
            print(f"Full traceback: {traceback.format_exc()}")
            self.close()
        
        return True
    
    def save(self):
        """Save the artifact and close the modal."""
        # Debug: Check if button is visible and clickable
        try:
            # Find the submit button directly
            submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            print(f"Submit button found: {submit_button.text}")
            print(f"Button visible: {submit_button.is_displayed()}")
            print(f"Button enabled: {submit_button.is_enabled()}")
            
            # Try to scroll the button into view
            self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
            
            # Wait a moment for scroll to complete
            time.sleep(1)
            
            # Try clicking with JavaScript first (more reliable)
            self.driver.execute_script("arguments[0].click();", submit_button)
            print("Button clicked successfully with JavaScript")
            
        except Exception as e:
            print(f"Error with submit button: {e}")
            # Fallback to original method
        self.submit_button.click()
        
        # Wait for modal to close (modal should disappear)
        self.clear()
    
    def cancel(self):
        """Cancel artifact creation and close the modal."""
        try:
            # Click the cancel button
            self.cancel_button.click()
            print("Cancel button clicked successfully")
        except Exception as e:
            print(f"Error clicking cancel button: {e}")
            # Fallback: try to find and click the cancel button directly
            try:
                cancel_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Cancel')]")
                cancel_button.click()
                print("Cancel button clicked via direct find")
            except Exception as e2:
                print(f"Error with fallback cancel button click: {e2}")
        
        # Wait a moment for the JavaScript to execute
        time.sleep(2)
        
        # Check if modal is still visible and try to close it
        try:
            modal = self.driver.find_element(By.ID, "artifactModal")
            if modal.is_displayed():
                print("Modal is still visible after cancel button click, forcing closure...")
                
                # Try to directly hide the modal via JavaScript
                try:
                    self.driver.execute_script("""
                        const modal = document.getElementById('artifactModal');
                        if (modal) {
                            modal.style.display = 'none';
                            modal.style.visibility = 'hidden';
                        }
                    """)
                    print("Modal forcibly hidden via JavaScript")
                    time.sleep(1)
                except Exception as e:
                    print(f"Error hiding modal directly: {e}")
            else:
                print("Modal closed successfully after cancel button click")
        except Exception as e:
            print(f"Modal element not found or error checking modal visibility: {e}")
        
        return True
    
    def abort(self):
        """Abort artifact creation (same as cancel)."""
        return self.cancel()
    
    def is_open(self):
        """Check if the editor modal is currently open."""
        try:
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
        self.locate(timeout)
        return True
    
    def clear(self, timeout=2):
        """Clear/clean up UI state (e.g., close modals, clear forms)."""
        from controls.base import ControlBase
        try:
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.invisibility_of_element_located((By.ID, "artifactModal")))
        except Exception as e:
            # If modal doesn't close automatically, show full error and force close it
            print(f"Modal did not close automatically. Full error: {str(e)}")
            print(f"Exception type: {type(e).__name__}")
            import traceback
            print(f"Full traceback: {traceback.format_exc()}")
            self.close()
        
        return True
        
        # Create a temporary ControlBase instance to use its clear method
        temp_control = ControlBase("")
        return temp_control.clear(self.driver, timeout)
