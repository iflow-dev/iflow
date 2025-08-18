"""
Base control class for BDD test automation.
This module provides the foundation for all page object pattern classes.
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
