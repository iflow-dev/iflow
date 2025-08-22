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


class Artifacts:
    """Class for finding artifacts on the page."""
    
    def __init__(self, driver=None):
        """Initialize with optional driver."""
        self.driver = driver
    
    def wait(self, timeout=10):
        """Wait for the artifacts container to be visible."""
        if self.driver is None:
            from radish import world
            self.driver = world.driver
        
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located((By.ID, "artifacts-container")))
    
    def find(self, id=None, summary=None, key=None):
        """Find artifacts on the page based on id, summary, or key."""
        if self.driver is None:
            from radish import world
            self.driver = world.driver
        
        artifacts = []
        try:
            container = self.wait()
            # Look for individual artifact elements - try different selectors
            artifact_elements = container.find_elements(By.CSS_SELECTOR, ".artifact-tile")
            
            # If no .artifact-tile elements found, try alternative selectors
            if not artifact_elements:
                artifact_elements = container.find_elements(By.CSS_SELECTOR, "[id^='artifact-']")
            
            if not artifact_elements:
                artifact_elements = container.find_elements(By.CSS_SELECTOR, ".artifact")
            
            if not artifact_elements:
                # Last resort: look for any div that might be an artifact
                artifact_elements = container.find_elements(By.CSS_SELECTOR, "div")
                # Filter to only divs that look like artifacts (have some content)
                artifact_elements = [elem for elem in artifact_elements if elem.text.strip()]
            
            log.info(f"Found {len(artifact_elements)} potential artifact elements")
            
            for element in artifact_elements:
                element_text = element.text.strip()
                if not element_text:  # Skip empty elements
                    continue
                    
                log.info(f"Element text: '{element_text[:100]}...'")
                
                # Apply filters if specified
                if id and str(id) in element_text:
                    artifacts.append(element)
                elif summary and summary in element_text:
                    artifacts.append(element)
                elif key and key in element_text:
                    artifacts.append(element)
                elif not id and not summary and not key:
                    # No filters, include all
                    artifacts.append(element)
                    
            log.info(f"Returning {len(artifacts)} artifacts after filtering")
        
        except Exception as e:
            log.debug(f"Error finding artifacts: {e}")
        
        return artifacts
