"""
Article control class for artifact operations.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from radish import world


class Article:
    """Article control class for artifact operations."""
    
    def __init__(self, element=None):
        self.element = element
    
    @property
    def flag(self):
        """Return a flag object that provides flag-related properties and methods."""
        return Flag(self)
    
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
        current_state = self.flag.active
        
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
                editor = Editor()
                editor.clear()
            except:
                pass
        
        return current_state


class Flag:
    """Flag object that provides flag-related properties and methods."""
    
    def __init__(self, article):
        self.article = article
    
    @property
    def active(self):
        """Get the current flag state as a boolean."""
        if not self.article.element:
            raise Exception("No artifact element available")
        
        # Get the current flag state of an artifact
        artifact_element = self.article.element
        if not artifact_element:
            raise Exception("No artifact element provided")
            
        flag_button = artifact_element.find_element(By.CSS_SELECTOR, ".artifact-actions button:first-child")
        icon = flag_button.find_element(By.CSS_SELECTOR, "ion-icon")
        icon_name = icon.get_attribute("name")
        return "outline" not in icon_name



