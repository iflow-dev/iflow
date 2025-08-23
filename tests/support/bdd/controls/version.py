from selenium.webdriver.common.by import By
from .base import ControlBase


class Header(ControlBase):
    """Control for header elements."""
    
    def __init__(self):
        super().__init__("//header")
    
    @property
    def version(self):
        """Get version information from header."""
        try:
            element = self.locate().find_element(By.ID, "header-version")
            return element.text.strip()
        except:
            return None


class StatisticsLine(ControlBase):
    """Control for statistics line elements."""
    
    def __init__(self):
        super().__init__("//div[@id='stats-bar']")
    
    @property
    def text(self):
        """Get statistics line text."""
        try:
            return self.locate().text.strip()
        except:
            return None
    
    @property
    def is_visible(self):
        """Check if statistics line is visible."""
        try:
            return self.locate().is_displayed()
        except:
            return False
    
    def contains_version(self):
        """Check if statistics line contains version information."""
        text = self.text
        if not text:
            return False
        
        # Check for version patterns
        import re
        version_pattern = r'v\d+\.\d+\.\d+'
        if re.search(version_pattern, text):
            return True
        
        # Check for simple version indicators
        if "version" in text.lower():
            return True
        
        # Check for v + digit pattern
        if "v" in text and any(char.isdigit() for char in text):
            return True
        
        return False
