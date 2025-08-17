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
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        wait = WebDriverWait(driver, timeout)
        return wait.until(EC.presence_of_element_located((By.XPATH, self.xpath)))

    def get_text(self, driver, timeout=5):
        return self.locate(driver, timeout).text
        
    def exists(self, driver, timeout=5):
        """Wait for element to appear and return true/false."""
        try:
            self.locate(driver, timeout)
            return True
        except:
            return False


class Title(ControlBase):
    def __init__(self, text):
        super().__init__(f"//h1[contains(text(), '{text}')]")


class Navigation(ControlBase):
    def __init__(self, driver):
        super().__init__("//nav")
