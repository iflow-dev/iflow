"""
ArtifactTile control class for BDD test automation.
This module provides controls for managing individual artifact tiles.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base import ControlBase


class ArtifactTile(ControlBase):
    """Control for individual artifact tile elements."""

    def __init__(self, element):
        """Initialize with a specific tile element."""
        super().__init__(None)  # No selector needed, we have the element
        self._element = element

    def locate(self):
        """Return the tile element directly."""
        return self._element

    def find_edit_button(self):
        """Find the edit button within this tile."""
        try:
            return self._element.find_element(By.CSS_SELECTOR, "button[onclick*='openEditModal']")
        except:
            return None

    def get_status_text(self):
        """Get the status text from this tile."""
        try:
            status_element = self._element.find_element(By.CSS_SELECTOR, ".artifact-status span, .artifact-status")
            return status_element.text.strip().lower()
        except:
            return None

    def scroll_edit_button_into_view(self):
        """Scroll the edit button into view for better interaction."""
        edit_button = self.find_edit_button()
        if edit_button:
            from selenium.webdriver.common.action_chains import ActionChains
            actions = ActionChains(self._element.parent)
            actions.move_to_element(edit_button).perform()
        return edit_button

    def click_edit_button(self, driver):
        """Click the edit button with fallback to JavaScript if needed."""
        edit_button = self.find_edit_button()
        if not edit_button:
            raise ValueError("Edit button not found in artifact tile")

        # Scroll into view first
        self.scroll_edit_button_into_view()

        # Wait for button to be clickable
        wait = WebDriverWait(driver, 10)
        wait.until(EC.element_to_be_clickable(edit_button))

        # Try regular click first, fallback to JavaScript
        try:
            edit_button.click()
            return True
        except Exception as e:
            # Fallback to JavaScript click
            driver.execute_script("arguments[0].click();", edit_button)
            return True
