"""
Base control class for BDD test automation.
This module provides the foundation for all page object pattern classes.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from radish import world

# Default timeout for element operations (in seconds)
DEFAULT_TIMEOUT = 5


class ControlBase:
    # Class-level debug mode flag - can be toggled at runtime
    DEBUG_MODE = False
    
    def __init__(self, xpath):
        self.xpath = xpath
    
    @classmethod
    def set_debug_mode(cls, enabled):
        """Enable or disable debug mode for all controls."""
        cls.DEBUG_MODE = enabled
        print(f"🔧 ControlBase debug mode: {'ON' if enabled else 'OFF'}")
    
    @classmethod
    def enable_debug_for_test(cls):
        """Enable debug mode for the current test run."""
        cls.set_debug_mode(True)
        print("🐛 Debug mode enabled for this test run")
    
    def _debug_log(self, message):
        """Log debug message if debug mode is enabled."""
        if self.__class__.DEBUG_MODE:
            print(f"🐛 [ControlBase] {message}")

    def locate(self, timeout=None):
        """Locate the element within timeout, assert if not found."""
        import logging
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        
        # Set default timeout if None is provided
        if timeout is None:
            timeout = DEFAULT_TIMEOUT
        
        logger.debug(f"Looking for element with XPath: {self.xpath}")

        wait = WebDriverWait(world.driver, timeout)
        try:
            element = wait.until(EC.presence_of_element_located((By.XPATH, self.xpath)))
            logger.debug(f"Found element: {element.text}...")
            return element
        except TimeoutException:
            raise TimeoutException(f"Element ({self.xpath}) not found within {timeout} seconds")

    def get_text(self, timeout=None):
        # Set default timeout if None is provided
        if timeout is None:
            timeout = DEFAULT_TIMEOUT
        return self.locate(timeout).text

    def exists(self, timeout=None):
        """Wait for element to appear and return true/false."""
        # Set default timeout if None is provided
        if timeout is None:
            timeout = DEFAULT_TIMEOUT
        try:
            self.locate(timeout)
            return True
        except TimeoutException:
            return False

    def click(self, timeout=None):
        """Click the element after locating it with enhanced debug handling."""
        # Set default timeout if None is provided
        if timeout is None:
            timeout = DEFAULT_TIMEOUT
        
        element = self.locate(timeout)
        element.click()
    
    def clear(self, timeout=None):
        """Clear/clean up UI state (e.g., close modals, clear forms)."""
        # Set default timeout if None is provided
        if timeout is None:
            timeout = DEFAULT_TIMEOUT
        
        try:
            # Wait for any modal to close if it was open
            wait = WebDriverWait(world.driver, timeout)
            wait.until_not(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".modal-content"))
            )
            return True
        except TimeoutException:
            # Modal might not be present, which is fine
            return False
