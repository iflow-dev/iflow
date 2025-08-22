"""
Artifact control classes for BDD test automation.
"""

from controls.base import ControlBase
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from radish import world
import logging

log = logging.getLogger(__name__)


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


class Artifacts:
    """Class for finding artifacts on the page."""
    
    def __init__(self):
        """Initialize Artifacts finder."""
        pass
    
    def wait(self, timeout=10):
        """Wait for the artifacts container to be visible."""
        wait = WebDriverWait(world.driver, timeout)
        return wait.until(EC.presence_of_element_located((By.ID, "artifacts-container")))
    
    def find(self, id=None, summary=None, key=None):
        """Find artifacts on the page based on id, summary, or key."""
        artifacts = []
        try:
            container = self.wait()
            # Look for individual artifact elements
            artifact_elements = container.find_elements(By.CSS_SELECTOR, ".artifact-tile")
            
            log.info(f"Found {len(artifact_elements)} artifact tiles")
            
            for element in artifact_elements:
                # Apply filters if specified
                if id:
                    # Look for artifact ID in the .artifact-id div
                    try:
                        id_div = element.find_element(By.CSS_SELECTOR, ".artifact-id")
                        displayed_id = id_div.text.strip()
                        log.debug(f"Checking artifact tile: displayed ID = '{displayed_id}', looking for '{id}'")
                        # Match the exact displayed value
                        if displayed_id == str(id):
                            artifacts.append(element)
                            continue
                    except:
                        # No .artifact-id div found, skip this element
                        log.debug(f"No .artifact-id div found in tile")
                        continue
                
                if summary:
                    # Look for summary in the .artifact-summary div
                    try:
                        summary_div = element.find_element(By.CSS_SELECTOR, ".artifact-summary")
                        if summary in summary_div.text.strip():
                            artifacts.append(element)
                            continue
                    except:
                        # No .artifact-summary div found, skip this element
                        continue
                
                if key:
                    # Look for key in any text content
                    if key in element.text.strip():
                        artifacts.append(element)
                        continue
                
                # If no filters specified, include all artifacts
                if not id and not summary and not key:
                    artifacts.append(element)
                    
            log.info(f"Returning {len(artifacts)} artifacts after filtering")
        
        except Exception as e:
            log.debug(f"Error finding artifacts: {e}")
        
        return artifacts
    
    def find_one(self, id=None, summary=None, key=None):
        """Find a single artifact and return an Artifact control object."""
        artifacts = self.find(id=id, summary=summary, key=key)
        if not artifacts:
            raise ValueError(f"No artifact found with id={id}, summary={summary}, key={key}")
        if len(artifacts) > 1:
            log.warning(f"Multiple artifacts found, using first one: {artifacts}")
        
        # Return the first matching artifact as an Artifact control object
        return Artifact.from_element(artifacts[0])
