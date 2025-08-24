from selenium.webdriver.common.by import By
from .base import ControlBase


class Header(ControlBase):
    """Control for header elements."""

    def __init__(self):
        super().__init__("//header")


class Footer(ControlBase):
    """Control for footer elements."""

    def __init__(self):
        super().__init__("//div[@id='status-line']")


class Version(ControlBase):
    """Control for version information elements."""

    def __init__(self):
        super().__init__("//span[@id='footer-version']")

    @property
    def text(self):
        """Get version information text."""
        try:
            element = self.locate()
            return element.text.strip()
        except Exception:
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
        except Exception:
            return None

    @property
    def is_visible(self):
        """Check if statistics line is visible."""
        try:
            return self.locate().is_displayed()
        except Exception:
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
