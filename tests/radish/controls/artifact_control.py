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
    
    def __init__(self, id=None, summary=None, element=None):
        self.artifact_id = id
        self.summary = summary
        self.element = element
        
        if element:
            # Store the element directly instead of creating an XPath
            super().__init__("//div")  # Dummy XPath, we'll use the stored element
        elif id:
            super().__init__(f"//div[@id='artifacts-container'][contains(., '{id}')]")
        elif summary:
            super().__init__(f"//div[@id='artifacts-container'][contains(., '{summary}')]")
        else:
            raise ValueError("Must provide either id, summary, or element")
    
    def locate(self, driver, timeout=5):
        """Locate the artifact element."""
        if self.element:
            # Return the stored element directly
            return self.element
        else:
            # Use the parent class's locate method
            return super().locate(timeout)
    
    @classmethod
    def from_element(cls, element):
        """Create an Artifact instance from a DOM element."""
        return cls(element=element)
    
    def exists(self, timeout=1):
        """Check if artifact exists within the specified timeout."""
        try:
            self.locate(timeout)
            return 1
        except Exception:
            return 0
    
    @property
    def id(self):
        """Get the artifact ID from the DOM element."""
        if not self.element:
            return self.artifact_id
        
        try:
            id_div = self.element.find_element(By.CSS_SELECTOR, ".artifact-id")
            return id_div.text.strip()
        except:
            return self.artifact_id
    
    @property
    def summary(self):
        """Get the artifact summary from the DOM element."""
        if not self.element:
            return self.summary
        
        try:
            summary_div = self.element.find_element(By.CSS_SELECTOR, ".artifact-summary")
            return summary_div.text.strip()
        except:
            return self.summary
    
    @property
    def text(self):
        """Get all text content from the artifact element."""
        if not self.element:
            return ""
        return self.element.text.strip()


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
