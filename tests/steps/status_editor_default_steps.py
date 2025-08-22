"""
Step definitions for testing status field default values in the editor.
This module tests that the status field properly shows default values and actual values.
"""

from radish import given, when, then, step, world
import logging
from controls.editor import Editor

# Set up logging
log = logging.getLogger(__name__)







@step("I see the editor is open")
def i_see_editor_is_open(step):
    """Verify that the artifact editor modal is open and visible."""
    editor = Editor(world.driver)
    editor.locate(world.driver)
    log.debug("Artifact editor modal is open and visible")

@step("I see the status is {expected_status:QuotedString}")
def i_see_status_is(step, expected_status):
    """Verify that the status field shows the expected status value."""
    editor = Editor(world.driver)
    actual_value = editor.get_status()
    
    if actual_value == expected_status:
        log.debug(f"Status field correctly shows expected status: {actual_value}")
    else:
        raise AssertionError(f"Expected status field to show '{expected_status}', but got '{actual_value}'")






@step("I open the artifact with {identifier:QuotedString}")
def i_open_artifact_with_identifier(step, identifier):
    """Open an artifact with the specified title or ID for editing."""
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    wait = WebDriverWait(world.driver, 10)
    
    # Try to find by ID first (if it looks like a number)
    if identifier.isdigit():
        # Look for artifact tile with data-artifact-id attribute
        xpath = f"//div[@class='artifact-tile' and @data-artifact-id='{identifier}']"
        try:
            artifact_tile = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            
            # Find the edit button within this tile
            edit_button = artifact_tile.find_element(By.CSS_SELECTOR, "button[onclick*='editArtifact'], button[onclick*='openEditModal']")
            edit_button.click()
            log.debug(f"Opened artifact with ID '{identifier}' for editing")
            return
            
        except Exception as e:
            log.debug(f"Could not find artifact with ID '{identifier}' using data-artifact-id: {e}")
            
            # Fallback: try looking for span with artifact-id class
            xpath_fallback = f"//span[@class='artifact-id' and text()='{identifier}']"
            try:
                artifact_id_span = wait.until(EC.presence_of_element_located((By.XPATH, xpath_fallback)))
                # Find the parent tile and then the edit button
                artifact_tile = artifact_id_span.find_element(By.XPATH, "./ancestor::div[contains(@class,'artifact-tile') or contains(@class,'artifact-card')]")
                edit_button = artifact_tile.find_element(By.CSS_SELECTOR, "button[onclick*='editArtifact'], button[onclick*='openEditModal']")
                edit_button.click()
                log.debug(f"Opened artifact with ID '{identifier}' for editing (fallback method)")
                return
            except Exception as e2:
                log.debug(f"Fallback method also failed: {e2}")
    else:
        # Find by title/summary using XPath
        xpath = f"//div[contains(@class,'artifact-tile') or contains(@class,'artifact-card')]//div[contains(@class,'artifact-summary') and text()='{identifier}']"
        try:
            summary_element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            
            # Find the parent tile and then the edit button
            artifact_tile = summary_element.find_element(By.XPATH, "./ancestor::div[contains(@class,'artifact-tile') or contains(@class,'artifact-card')]")
            edit_button = artifact_tile.find_element(By.CSS_SELECTOR, "button[onclick*='editArtifact'], button[onclick*='openEditModal']")
            edit_button.click()
            log.debug(f"Opened artifact with title '{identifier}' for editing")
            return
            
        except Exception as e:
            log.debug(f"Could not find artifact with title '{identifier}': {e}")
    
    raise AssertionError(f"No artifact found with identifier '{identifier}'")

# Note: Step "I set the status to {status:QuotedString}" is already defined in artifact_creation_steps.py



@step("I see artifact with {identifier:QuotedString} has status {status:QuotedString}")
def i_see_artifact_has_status(step, identifier, status):
    """Verify that the specified artifact has the expected status."""
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    wait = WebDriverWait(world.driver, 10)
    
    # Try to find by ID first (if it looks like a number)
    if identifier.isdigit():
        # Look for artifact tile with data-artifact-id attribute
        xpath = f"//div[@class='artifact-tile' and @data-artifact-id='{identifier}']"
        try:
            artifact_tile = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            
            # Find the status element within this tile
            status_element = artifact_tile.find_element(By.CSS_SELECTOR, ".artifact-status span, .artifact-status")
            actual_status = status_element.text.lower()
            
            assert actual_status == status.lower(), f"Expected artifact with ID '{identifier}' to have status '{status}', but got '{actual_status}'"
            log.debug(f"Verified artifact with ID '{identifier}' has status '{status}'")
            return
            
        except Exception as e:
            log.debug(f"Could not find artifact with ID '{identifier}' using data-artifact-id: {e}")
            
            # Fallback: try looking for span with artifact-id class
            xpath_fallback = f"//span[@class='artifact-id' and text()='{identifier}']"
            try:
                artifact_id_span = wait.until(EC.presence_of_element_located((By.XPATH, xpath_fallback)))
                # Find the parent tile and then the status
                artifact_tile = artifact_id_span.find_element(By.XPATH, "./ancestor::div[contains(@class,'artifact-tile') or contains(@class,'artifact-card')]")
                status_element = artifact_tile.find_element(By.CSS_SELECTOR, ".artifact-status span, .artifact-status")
                actual_status = status_element.text.lower()
                
                assert actual_status == status.lower(), f"Expected artifact with ID '{identifier}' to have status '{status}', but got '{actual_status}'"
                log.debug(f"Verified artifact with ID '{identifier}' has status '{status}' (fallback method)")
                return
            except Exception as e2:
                log.debug(f"Fallback method also failed: {e2}")
    else:
        # Find by title/summary using XPath
        xpath = f"//div[contains(@class,'artifact-tile') or contains(@class,'artifact-card')]//div[contains(@class,'artifact-summary') and text()='{identifier}']"
        try:
            summary_element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            
            # Find the parent tile and then the status
            artifact_tile = summary_element.find_element(By.XPATH, "./ancestor::div[contains(@class,'artifact-tile') or contains(@class,'artifact-card')]")
            status_element = artifact_tile.find_element(By.CSS_SELECTOR, ".artifact-status span, .artifact-status")
            actual_status = status_element.text.lower()
            
            assert actual_status == status.lower(), f"Expected artifact with title '{identifier}' to have status '{status}', but got '{actual_status}'"
            log.debug(f"Verified artifact with title '{identifier}' has status '{status}'")
            return
            
        except Exception as e:
            log.debug(f"Could not find artifact with title '{identifier}': {e}")
    
    raise AssertionError(f"No artifact found with identifier '{identifier}'")
