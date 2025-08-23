from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base import ControlBase


class VerificationField(ControlBase):
    """Control for verification field elements."""
    
    def __init__(self):
        super().__init__("//select[@id='artifactVerification']")
    
    @property
    def value(self):
        """Get current verification field value."""
        try:
            element = self.locate()
            return element.get_attribute("value")
        except:
            return None
    
    @property
    def is_visible(self):
        """Check if verification field is visible."""
        try:
            return self.locate().is_displayed()
        except:
            return False
    
    @property
    def is_enabled(self):
        """Check if verification field is enabled."""
        try:
            return self.locate().is_enabled()
        except:
            return False
    
    def set_value(self, value):
        """Set verification field value."""
        element = self.locate()
        element.clear()
        element.send_keys(value)


class ArtifactForm(ControlBase):
    """Control for artifact form fields."""
    
    def __init__(self):
        super().__init__("//form")
    
    def set_summary(self, summary):
        """Set artifact summary field."""
        summary_field = self.locate().find_element(By.ID, "artifactSummary")
        summary_field.clear()
        summary_field.send_keys(summary)
    
    def set_description(self, description):
        """Set artifact description field."""
        description_field = self.locate().find_element(By.ID, "artifactDescription")
        description_field.clear()
        description_field.send_keys(description)


class ArtifactVerification(ControlBase):
    """Control for artifact verification display."""
    
    def __init__(self):
        super().__init__("//div[contains(@class, 'artifact-verification')]")
    
    @property
    def text(self):
        """Get verification method text."""
        try:
            return self.locate().text.strip()
        except:
            return None
    
    @property
    def is_visible(self):
        """Check if verification method is visible."""
        try:
            return self.locate().is_displayed()
        except:
            return False
    
    def contains_method(self, method):
        """Check if verification method contains specific value."""
        text = self.text
        return text and method in text if text else False


class SuccessIndicator(ControlBase):
    """Control for success message indicators."""
    
    def __init__(self):
        super().__init__("//div[@class='artifacts-container']")
    
    def wait_for_success(self, timeout=10):
        """Wait for success indicator to appear."""
        wait = WebDriverWait(world.driver, timeout)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "artifacts-container")))
