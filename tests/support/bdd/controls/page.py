"""
Page control class for common page operations.
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from radish import world
from controls.artifact import Artifacts


class Page:
    """Page control class for common page operations."""

    def __init__(self):
        pass

    @property
    def artifacts(self):
        """Return an Artifacts instance for finding artifacts on the page."""
        return Artifacts()

    def wait(self, timeout=10):
        """ Waits for the "loading text in view to disappear"""
        WebDriverWait(world.driver, timeout).until(
            EC.invisibility_of_element_located((By.XPATH, "//*[contains(text(), 'Loading...')]"))
        )
        return WebDriverWait(world.driver, timeout)


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

    def clear_modal(self):
        """Close any open modal to ensure clean state."""
        try:
            modal = world.driver.find_element(By.ID, "artifactModal")
            if modal.is_displayed():
                # Try to find and click the close button (×)
                close_button = world.driver.find_element(By.XPATH, "//div[@id='artifactModal']//button[contains(text(), '×') or contains(@class, 'close')]")
                close_button.click()
                # Wait for modal to close
                WebDriverWait(world.driver, 5).until(EC.invisibility_of_element_located((By.ID, "artifactModal")))
                return True
        except Exception:
            # No modal to close or error closing modal
            pass
        return False
