"""
Simple control classes for BDD test automation.
This module provides basic controls for common UI elements.
"""

import sys
import os
# Add the tests directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from controls.base import ControlBase


class Title(ControlBase):
    """Control for locating page titles."""
    def __init__(self, text):
        super().__init__(f"//h1[contains(text(), '{text}')]")


class Navigation(ControlBase):
    """Control for locating navigation elements."""
    def __init__(self, driver):
        super().__init__("//nav")


class Tile(ControlBase):
    """Control for locating artifact tiles."""
    def __init__(self, tile_id):
        super().__init__(f"//div[@class='artifact-card' and contains(., '{tile_id}')]")


class StatusLine(ControlBase):
    """Control for the status line that shows artifact count."""
    def __init__(self):
        super().__init__("//div[@class='status-line']")
    
    def get_total_artifacts(self, driver, timeout=5):
        """Extract the total number of artifacts from the status line."""
        text = self.get_text(driver, timeout)
        import re
        # Look for a number at the beginning of the status line
        match = re.search(r'^(\d+)', text)
        if match:
            return int(match.group(1))
        else:
            raise ValueError(f"Could not extract artifact count from status line: '{text}'")
