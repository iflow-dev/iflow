"""
Artifact control classes for BDD test automation.
"""

from controls.base import ControlBase
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

log = logging.getLogger(__name__)


class Artifact(ControlBase):
    """Control for locating and interacting with individual artifacts."""
    
    def __init__(self, id=None, summary=None, element_id=None):
        self.artifact_id = id
        self.summary = summary
        self.element_id = element_id
        
        if element_id:
            super().__init__(f"//div[@id='{element_id}']")
        elif id:
            super().__init__(f"//div[@id='artifacts-container'][contains(., '{id}')]")
        elif summary:
            super().__init__(f"//div[@id='artifacts-container'][contains(., '{summary}')]")
        else:
            raise ValueError("Must provide either id, summary, or element_id")
    
    @classmethod
    def from_element_id(cls, element_id):
        """Create an Artifact instance from an element ID."""
        return cls(element_id=element_id)
    
    def exists(self, timeout=1):
        """Check if artifact exists within the specified timeout."""
        try:
            from radish import world
            self.locate(world.driver, timeout)
            return 1
        except Exception:
            return 0


class ArtifactFinder:
    """Class for finding artifacts on the page."""
    
    @staticmethod
    def find(key=None, summary=None, driver=None):
        """Find artifacts on the page based on key or summary."""
        if driver is None:
            from radish import world
            driver = world.driver
        
        artifacts = []
        
        try:
            wait = WebDriverWait(driver, 10)
            container = wait.until(EC.presence_of_element_located((By.ID, "artifacts-container")))
            container_text = container.text.strip()
            
            if key and key in container_text:
                artifact = Artifact(id=key)
                artifacts.append(artifact)
            
            if summary and summary in container_text:
                artifact = Artifact(summary=summary)
                artifacts.append(artifact)
            
        except Exception as e:
            log.debug(f"Error finding artifacts: {e}")
        
        return artifacts
