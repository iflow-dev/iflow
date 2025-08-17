"""
Control classes for BDD test automation.
This module provides page object pattern classes for interacting with web elements.
"""

from selenium.webdriver.common.by import By


class ControlBase:
    def __init__(self, xpath):
        self.xpath = xpath

    def locate(self, driver, timeout=5):
        """Locate the element within timeout, assert if not found."""
        import logging
        logging.basicConfig(level=logging.DEBUG)
        logger = logging.getLogger(__name__)
        
        logger.debug(f"Looking for element with XPath: {self.xpath}")
        
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        wait = WebDriverWait(driver, timeout)
        element = wait.until(EC.presence_of_element_located((By.XPATH, self.xpath)))
        
        logger.debug(f"Found element: {element.text[:100]}...")
        return element

    def get_text(self, driver, timeout=5):
        return self.locate(driver, timeout).text
        
    def exists(self, driver, timeout=5):
        """Wait for element to appear and return true/false."""
        try:
            self.locate(driver, timeout)
            return True
        except:
            return False
    
    def click(self, driver, timeout=5):
        """Click the element after locating it."""
        element = self.locate(driver, timeout)
        element.click()
        return element


class Title(ControlBase):
    def __init__(self, text):
        super().__init__(f"//h1[contains(text(), '{text}')]")


class Navigation(ControlBase):
    def __init__(self, driver):
        super().__init__("//nav")


class Tile(ControlBase):
    def __init__(self, tile_id):
        super().__init__(f"//div[@class='artifact-card' and contains(., '{tile_id}')]")


class Button(ControlBase):
    """Control for locating and interacting with buttons."""
    
    def __init__(self, text):
        """
        Initialize button control with text content.
        
        Args:
            text: Button text content (e.g., "Create", "Save", "Cancel")
        """
        xpath = f"//button[contains(text(), '{text}')]"
        super().__init__(xpath)


class Modal(ControlBase):
    """Control for locating and interacting with modal dialogs."""
    
    def __init__(self, identifier=None):
        """
        Initialize modal control.
        
        Args:
            identifier: Optional identifier for the modal (text, class, or id)
        """
        if identifier:
            xpath = f"//div[contains(@class, 'modal') and contains(., '{identifier}')]"
        else:
            xpath = "//div[contains(@class, 'modal')]"
        super().__init__(xpath)
    
    def is_visible(self, driver, timeout=5):
        """Check if the modal is currently visible."""
        try:
            element = self.locate(driver, timeout)
            return element.is_displayed()
        except:
            return False
    
    def wait_for_visible(self, driver, timeout=5):
        """Wait for modal to become visible."""
        element = self.locate(driver, timeout)
        if not element.is_displayed():
            raise AssertionError(f"Modal found but not visible after {timeout} seconds")
        return element
