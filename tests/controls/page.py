"""
Page control class for common page operations.
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class Page:
    """Page control class for common page operations."""
    
    def __init__(self, driver):
        self.driver = driver
    
    def wait(self, timeout=10):
        """ Waits for the "loading text in view to disappear"""
        WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located((By.XPATH, "//*[contains(text(), 'Loading...')]"))
        )
        return WebDriverWait(self.driver, timeout)

    
    def wait_for_element_visible(self, by, value, timeout=10):
        """Wait for an element to be visible."""
        wait = self.wait(timeout)
        return wait.until(EC.visibility_of_element_located((by, value)))
    
    def wait_for_elements(self, by, value, timeout=10):
        """Wait for multiple elements to be present."""
        wait = self.wait(timeout)
        return wait.until(EC.presence_of_all_elements_located((by, value)))
    
    def wait_for_element_invisible(self, by, value, timeout=10):
        """Wait for an element to become invisible."""
        wait = self.wait(timeout)
        return wait.until(EC.invisibility_of_element_located((by, value)))
