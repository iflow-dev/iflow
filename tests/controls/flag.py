from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from controls.base import ControlBase


class Flag(ControlBase):
    """Control class for flag operations."""
    
    def __init__(self, driver):
        """Initialize the Flag control.
        
        Args:
            driver: WebDriver instance
        """
        super().__init__("flagCheckbox")
        self.driver = driver
    
    @property
    def state(self):
        """Get the current flag state."""
        element = self.find_element(self.driver)
        return element.is_selected()
    
    def toggle(self, active=None):
        """Toggle the flag state.
        
        Args:
            active: 
                - None: toggle the current state
                - True: ensure flag is on (flagged)
                - False: ensure flag is off (unflagged)
        
        Returns:
            bool: The new flag state after toggling
        """
        element = self.find_element(self.driver)
        current_state = element.is_selected()
        
        should_click = False
        if active is None:
            should_click = True
        elif active and not current_state:
            should_click = True
        elif not active and current_state:
            should_click = True
        
        if should_click:
            element.click()
            # Wait a moment for the state to update
            WebDriverWait(self.driver, 2).until(
                lambda d: element.is_selected() != current_state
            )
        
        return element.is_selected()
    
    def set(self, active):
        """Set the flag to a specific state.
        
        Args:
            active: True to flag, False to unflag
        
        Returns:
            bool: The new flag state
        """
        return self.toggle(active=active)
    
    def check(self):
        """Check (flag) the article."""
        return self.set(True)
    
    def uncheck(self):
        """Uncheck (unflag) the article."""
        return self.set(False)
