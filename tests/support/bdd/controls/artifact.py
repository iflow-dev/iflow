"""
Artifact control classes for BDD test automation.
"""

from controls.base import ControlBase
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from radish import world
from logging_config import logger


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
        try:
            id_div = self._element.find_element(By.CSS_SELECTOR, ".artifact-id")
            return id_div.text.strip()
        except:
            return None

    @property
    def summary(self):
        """Get the artifact summary from the DOM element."""
        try:
            summary_div = self._element.find_element(By.CSS_SELECTOR, ".artifact-summary")
            return summary_div.text.strip()
        except:
            return None

    @property
    def text(self):
        """Get all text content from the artifact element."""
        return self._element.text.strip()

    @property
    def status(self):
        """Get the artifact status from the DOM element."""
        try:
            status_div = self._element.find_element(By.CSS_SELECTOR, ".artifact-status span")
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
        """Wait for the artifacts container to be visible and populated."""
        wait = WebDriverWait(world.driver, timeout)
        # Wait for container
        wait.until(EC.presence_of_element_located((By.ID, "artifacts-container")))

        # Wait for at least one artifact tile to be present (not just loading message)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".artifact-tile")))

        # Additional wait to ensure artifacts are fully rendered
        wait.until(lambda driver: len(driver.find_elements(By.CSS_SELECTOR, ".artifact-tile")) > 0)

        return self

    def find(self, id=None, summary=None, key=None):
        """Find artifacts on the page based on id, summary, or key."""
        artifacts = []
        try:
            # Wait for container and artifacts to be fully loaded
            self.wait()
            container = world.driver.find_element(By.ID, "artifacts-container")

            # Look for individual artifact elements
            artifact_elements = container.find_elements(By.CSS_SELECTOR, ".artifact-tile")

            for element in artifact_elements:
                # Create Artifact instance first
                artifact = Artifact.from_element(element)

                # Apply filters if specified
                if id is not None:
                    artifact_id = artifact.id
                    if artifact_id is None or str(artifact_id) != str(id):
                        continue

                if summary is not None:
                    artifact_summary = artifact.summary
                    if artifact_summary is None or summary not in artifact_summary:
                        continue

                if key is not None:
                    artifact_text = artifact.text
                    if artifact_text is None or key not in artifact_text:
                        continue

                # Add the artifact to results
                artifacts.append(artifact)

        except Exception as e:
            # Log the error for debugging
            log.trace(f"Error in Artifacts.find(): {e}")
            pass

        return artifacts

    def find_one(self, id=None, summary=None, key=None):
        """Find a single artifact and return an Artifact control object."""
        artifacts = self.find(id=id, summary=summary, key=key)
        if not artifacts:
            raise ValueError(f"No artifact found with id={id}, summary={summary}, key={key}")
        if len(artifacts) > 1:
            log.trace(f"Warning: Multiple artifacts found ({len(artifacts)}), using first one")

        # Return the first matching artifact
        return artifacts[0]
