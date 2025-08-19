"""
Base control class for BDD test automation.
This module provides the foundation for all page object pattern classes.
"""

from selenium.webdriver.common.by import By


class ControlBase:
    def __init__(self, xpath):
        self.xpath = xpath

    def locate(self, driver, timeout=None):
        """Locate the element within timeout, assert if not found."""
        import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
        
        # Set default timeout if None is provided
        if timeout is None:
            timeout = 5
        
        logger.debug(f"Looking for element with XPath: {self.xpath}")

        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        wait = WebDriverWait(driver, timeout)
        element = wait.until(EC.presence_of_element_located((By.XPATH, self.xpath)))

        logger.debug(f"Found element: {element.text}...")
        return element

    def get_text(self, driver, timeout=None):
        # Set default timeout if None is provided
        if timeout is None:
            timeout = 5
        return self.locate(driver, timeout).text

    def exists(self, driver, timeout=None):
        """Wait for element to appear and return true/false."""
        # Set default timeout if None is provided
        if timeout is None:
            timeout = 5
        try:
            self.locate(driver, timeout)
            return True
        except:
            return False

    def click(self, driver, timeout=None):
        """Click the element after locating it."""
        # Set default timeout if None is provided
        if timeout is None:
            timeout = 5
        element = self.locate(driver, timeout)
        element.click()
        return element
