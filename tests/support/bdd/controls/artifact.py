"""
Artifact control classes for BDD test automation.
"""

from controls.base import ControlBase
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from radish import world


class Artifact(ControlBase):
    """Control for locating and interacting with individual artifacts."""
    
    def __init__(self, element):
        self._element = element
        # Store the element directly instead of creating an XPath
        super().__init__("//div")  # Dummy XPath, we'll use the stored element
    
    def locate(self, timeout=5):
        """Locate the artifact element."""
        return self._element
    
    @classmethod
    def from_element(cls, element):
        """Create an Artifact instance from a DOM element."""
        return cls(element)
    
    @property
    def id(self):
        """Get the artifact ID from the DOM element."""
        id_div = self._element.find_element(By.CSS_SELECTOR, ".artifact-id")
        return id_div.text.strip()
    
    @property
    def summary(self):
        """Get the artifact summary from the DOM element."""
        summary_div = self._element.find_element(By.CSS_SELECTOR, ".artifact-summary")
        return summary_div.text.strip()
    
    @property
    def text(self):
        """Get all text content from the artifact element."""
        return self._element.text.strip()
    
    @property
    def status(self):
        """Get the artifact status from the DOM element."""
        try:
            status_div = self._element.find_element(By.CSS_SELECTOR, ".artifact-status")
            status_text = status_div.text.strip()
            
            # Return None for values that indicate no status is set
            if not status_text or status_text == "None" or status_text == "All":
                return None
                
            return status_text
        except:
            return None


class Artifacts:
    """Class for finding artifacts on the page."""
    
    def __init__(self):
        """Initialize Artifacts finder."""
        pass
    
    def wait(self, timeout=10):
        """Wait for the artifacts container to be visible."""
        wait = WebDriverWait(world.driver, timeout)
        wait.until(EC.presence_of_element_located((By.ID, "artifacts-container")))
        return self
    
    def find(self, id=None, summary=None, key=None):
        """Find artifacts on the page based on id, summary, or key."""
        artifacts = []
        try:
            # Wait for container and get it
            self.wait()
            container = world.driver.find_element(By.ID, "artifacts-container")
            # Look for individual artifact elements
            artifact_elements = container.find_elements(By.CSS_SELECTOR, ".artifact-tile")
            
            for element in artifact_elements:
                # Create Artifact instance first
                artifact = Artifact.from_element(element)
                
                # Apply filters if specified
                if id and artifact.id != str(id):
                    continue
                    
                if summary and summary not in artifact.summary:
                    continue
                    
                if key and key not in artifact.text:
                    continue
                
                # Add the artifact to results
                artifacts.append(artifact)
        
        except Exception:
            pass
        
        return artifacts
    
    def find_one(self, id=None, summary=None, key=None):
        """Find a single artifact and return an Artifact control object."""
        artifacts = self.find(id=id, summary=summary, key=key)
        if not artifacts:
            raise ValueError(f"No artifact found with id={id}, summary={summary}, key={key}")
        if len(artifacts) > 1:
            pass  # Use first one
        
        # Return the first matching artifact
        return artifacts[0]
