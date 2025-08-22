"""
Simple control classes for BDD test automation.
This module provides basic controls for common UI elements.
"""

import sys
import os
# Add the tests directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .base import ControlBase


class Title(ControlBase):
    """Control for locating page titles."""
    def __init__(self, text):
        super().__init__(f"//h1[contains(text(), '{text}')]")


class Navigation(ControlBase):
    """Control for locating navigation elements."""
    def __init__(self):
        super().__init__("//nav")


class Tile(ControlBase):
    """Control for locating artifact tiles."""
    def __init__(self, tile_id):
        # Store the tile_id for use in locate method
        self.tile_id = tile_id
        # The artifacts are displayed directly in the container, not as .artifact-card elements
        # Look for the content anywhere in the artifacts container
        super().__init__(f"//div[@id='artifacts-container'][contains(., '{tile_id}')]")
    
    def locate(self, timeout=5):
        """Override locate to handle the case where artifacts are displayed as text, not as cards."""
        try:
            # First try to find the content in the artifacts container
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            
            from radish import world
            wait = WebDriverWait(world.driver, timeout)
            container = wait.until(EC.presence_of_element_located((By.ID, "artifacts-container")))
            
            # Check if the container contains our search text
            if self.tile_id in container.text:
                return container
            else:
                raise Exception(f"Content '{self.tile_id}' not found in artifacts container")
                
        except Exception as e:
            # Fall back to the original method
            return super().locate(timeout)


class StatusLine(ControlBase):
    """Control for the status line that shows artifact count."""
    def __init__(self):
        super().__init__("//div[@class='status-line']")
    
    def get_total_artifacts(self, timeout=5):
        """Extract the total number of artifacts from the status line."""
        text = self.get_text(timeout)
        import re
        # Look for a number at the beginning of the status line
        match = re.search(r'^(\d+)', text)
        if match:
            return int(match.group(1))
        else:
            raise ValueError(f"Could not extract artifact count from status line: '{text}'")
