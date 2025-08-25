"""
Button control for BDD test automation.
This module provides controls for button elements.
"""

import sys
import os
# Add the tests directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from controls.base import ControlBase


class Button(ControlBase):
    """Control for locating and interacting with buttons."""

    def __init__(self, type, text, icon):
        """
        Initialize button control with type, text, and icon.

        Args:
            type: Button type (e.g., "submit", "icon")
            text: Button text content (e.g., "Create", "Save", "Cancel")
            icon: Icon name for icon-based buttons (e.g., "create-outline")
        """
        if type == "submit":
            if text:
                xpath = f"//button[@type='submit' and contains(text(), '{text}')]"
            else:
                xpath = "//button[@type='submit']"  # Any submit button regardless of text
        elif type == "icon":
            xpath = f"//button[.//img[contains(@src, '{icon}')]]"
        else:
            if text:
                xpath = f"//button[contains(text(), '{text}')]"
            else:
                xpath = "//button"  # Any button regardless of text

        super().__init__(xpath)
