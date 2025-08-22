"""
Modal control for BDD test automation.
This module provides controls for modal dialogs.
"""

import sys
import os
# Add the tests directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from controls.base import ControlBase


class Modal(ControlBase):
    """Control for locating and interacting with modal dialogs."""
    
    def __init__(self, identifier=None):
        """
        Initialize modal control.
        
        Args:
            identifier: Optional identifier for the modal (text, class, or id)
        """
        if identifier == "create":
            # For create modal, look for modal with "Create New Artifact" title
            xpath = "//div[@id='artifactModal' and @class='modal']"
        elif identifier:
            xpath = f"//div[contains(@class, 'modal') and contains(., '{identifier}')]"
        else:
            xpath = "//div[contains(@class, 'modal')]"
        super().__init__(xpath)
    
    def is_visible(self, timeout=5):
        """Check if the modal is currently visible."""
        try:
            element = self.locate(timeout)
            return element.is_displayed()
        except:
            return False
    
    def wait_for_visible(self, timeout=5):
        """Wait for modal to become visible."""
        element = self.locate(timeout)
        if not element.is_displayed():
            raise AssertionError(f"Modal found but not visible after {timeout} seconds")
        return element
