"""
Article control class for artifact operations.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class Article:
    """Article control class for artifact operations."""
    
    def __init__(self, driver, element=None):
        self.driver = driver
        self.element = element
    
    def toggle(self, active=None):
        """Toggle the flag state of this artifact.
        
        Args:
            active: 
                - None: toggle the current state
                - True: ensure flag is on (flagged)
                - False: ensure flag is off (unflagged)
        """
        if not self.element:
            raise Exception("No artifact element available")
        
        # Get current flag state
        current_state = self.get_flag_state(self.element)
        
        # Determine if we need to click the button
        should_click = False
        
        if active is None:
            # Toggle mode: always click to change state
            should_click = True
        elif active and not current_state:
            # Ensure on: click if currently off
            should_click = True
        elif not active and current_state:
            # Ensure off: click if currently on
            should_click = True
        
        # Click the button if needed
        if should_click:
            # Find and click the flag button
            flag_button = self.element.find_element(By.CSS_SELECTOR, ".artifact-actions button:first-child")
            flag_button.click()
            
            # Wait for any modal to close if it was open
            try:
                from controls.editor import Editor
                editor = Editor(self.driver)
                editor.clear()
            except:
                pass
        
        return current_state
    
    def get_flag_state(self, artifact_element=None):
        """Get the current flag state of an artifact."""
        element = artifact_element or self.element
        if not element:
            raise Exception("No artifact element provided")
            
        flag_button = element.find_element(By.CSS_SELECTOR, ".artifact-actions button:first-child")
        icon = flag_button.find_element(By.CSS_SELECTOR, "ion-icon")
        icon_name = icon.get_attribute("name")
        return "outline" not in icon_name
