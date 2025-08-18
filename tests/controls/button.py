"""
Button control class for BDD test automation.
This module provides controls for locating and interacting with buttons.
"""

from controls.base import ControlBase


class Button(ControlBase):
    """Control for locating and interacting with buttons."""
    
    def __init__(self, text, context=None):
        """
        Initialize button control with text content.
        
        Args:
            text: Button text content (e.g., "Create", "Save", "Cancel")
            context: Optional context to narrow down the search (e.g., "modal", "toolbar")
        """
        if context == "modal":
            # For buttons inside the modal, look within the modal context
            xpath = f"//div[@id='artifactModal']//button[contains(text(), '{text}')]"
        elif context == "toolbar":
            # For buttons in the toolbar, look in the toolbar context
            xpath = f"//div[@class='toolbar']//button[contains(text(), '{text}')]"
        else:
            # Default: look for any button with the text
            xpath = f"//button[contains(text(), '{text}')]"
        super().__init__(xpath)
