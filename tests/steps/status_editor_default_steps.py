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
            





@step("I open the artifact {artifact_id:w}")
def i_open_artifact_by_id(step, artifact_id):
    """Open an artifact with the specified ID (no quotes = ID search)."""
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    wait = WebDriverWait(world.driver, 10)
    
    # No quotes means search by ID
    # Look for artifact tile with data-artifact-id attribute
    xpath = f"//div[@class='artifact-tile' and @data-artifact-id='{artifact_id}']"
    try:
        artifact_tile = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        
        # Find the edit button within this tile
        edit_button = artifact_tile.find_element(By.CSS_SELECTOR, "button[onclick*='editArtifact'], button[onclick*='openEditModal']")
        edit_button.click()
        log.debug(f"Opened artifact with ID '{artifact_id}' for editing")
        return
        
    except Exception as e:
        log.debug(f"Could not find artifact with ID '{artifact_id}' using data-artifact-id: {e}")
        
        # Fallback: try looking for span with artifact-id class
        xpath_fallback = f"//span[@class='artifact-id' and text()='{artifact_id}']"
        try:
            artifact_id_span = wait.until(EC.presence_of_element_located((By.XPATH, xpath_fallback)))
            # Find the parent tile and then the edit button
            artifact_tile = artifact_id_span.find_element(By.XPATH, "./ancestor::div[contains(@class,'artifact-tile') or contains(@class,'artifact-card')]")
            edit_button = artifact_tile.find_element(By.CSS_SELECTOR, "button[onclick*='editArtifact'], button[onclick*='openEditModal']")
            edit_button.click()
            log.debug(f"Opened artifact with ID '{artifact_id}' for editing (fallback method)")
            return
        except Exception as e2:
            log.debug(f"Fallback method also failed: {e2}")
    
    raise AssertionError(f"No artifact found with ID '{artifact_id}'")

@step("I open the artifact {summary:QuotedString}")
def i_open_artifact_by_summary(step, summary):
    """Open an artifact with the specified title/summary (quotes = title search)."""
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    wait = WebDriverWait(world.driver, 10)
    
    # Quotes means search by title/summary
    xpath = f"//div[contains(@class,'artifact-tile') or contains(@class,'artifact-card')]//div[contains(@class,'artifact-summary') and text()='{summary}']"
    try:
        summary_element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        
        # Find the parent tile and then the edit button
        artifact_tile = summary_element.find_element(By.XPATH, "./ancestor::div[contains(@class,'artifact-tile') or contains(@class,'artifact-card')]")
        edit_button = artifact_tile.find_element(By.CSS_SELECTOR, "button[onclick*='editArtifact'], button[onclick*='openEditModal']")
        edit_button.click()
        log.debug(f"Opened artifact with title '{summary}' for editing")
        return
        
    except Exception as e:
        log.debug(f"Could not find artifact with title '{summary}': {e}")
    
    raise AssertionError(f"No artifact found with title '{summary}'")

# Note: Step "I set the status to {status:QuotedString}" is already defined in artifact_creation_steps.py

@step("I save the artifact")
def i_save_the_artifact(step):
    """Save the artifact using the Editor control."""
    from controls.editor import Editor
    
    # Create an Editor instance and save the article
    editor = Editor(world.driver)
    editor.save()



@step("I see artifact {artifact_id:w} has status {status:QuotedString}")
def i_see_artifact_has_status_by_id(step, artifact_id, status):
    """Verify that the specified artifact (by ID) has the expected status."""
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    wait = WebDriverWait(world.driver, 10)
    
    # No quotes means search by ID
    # Look for artifact tile with data-artifact-id attribute
    xpath = f"//div[@class='artifact-tile' and @data-artifact-id='{artifact_id}']"
    try:
        artifact_tile = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        
        # Find the status element within this tile
        status_element = artifact_tile.find_element(By.CSS_SELECTOR, ".artifact-status span, .artifact-status")
        actual_status = status_element.text.lower()
        
        assert actual_status == status.lower(), f"Expected artifact with ID '{artifact_id}' to have status '{status}', but got '{actual_status}'"
        log.debug(f"Verified artifact with ID '{artifact_id}' has status '{status}'")
        return
        
    except Exception as e:
        log.debug(f"Could not find artifact with ID '{artifact_id}' using data-artifact-id: {e}")
        
        # Fallback: try looking for span with artifact-id class
        xpath_fallback = f"//span[@class='artifact-id' and text()='{artifact_id}']"
        try:
            artifact_id_span = wait.until(EC.presence_of_element_located((By.XPATH, xpath_fallback)))
            # Find the parent tile and then the status
            artifact_tile = artifact_id_span.find_element(By.XPATH, "./ancestor::div[contains(@class,'artifact-tile') or contains(@class,'artifact-card')]")
            status_element = artifact_tile.find_element(By.CSS_SELECTOR, ".artifact-status span, .artifact-status")
            actual_status = status_element.text.lower()
            
            assert actual_status == status.lower(), f"Expected artifact with ID '{artifact_id}' to have status '{status}', but got '{actual_status}'"
            log.debug(f"Verified artifact with ID '{artifact_id}' has status '{status}' (fallback method)")
            return
        except Exception as e2:
            log.debug(f"Fallback method also failed: {e2}")
    
    raise AssertionError(f"No artifact found with ID '{artifact_id}'")

@step("I see artifact with {summary:QuotedString} has status {status:QuotedString}")
def i_see_artifact_has_status_by_summary(step, summary, status):
    """Verify that the specified artifact (by title) has the expected status."""
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    wait = WebDriverWait(world.driver, 10)
    
    # Quotes means search by title/summary
    xpath = f"//div[contains(@class,'artifact-tile') or contains(@class,'artifact-card')]//div[contains(@class,'artifact-summary') and text()='{summary}']"
    try:
        summary_element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        
        # Find the parent tile and then the status
        artifact_tile = summary_element.find_element(By.XPATH, "./ancestor::div[contains(@class,'artifact-tile') or contains(@class,'artifact-card')]")
        status_element = artifact_tile.find_element(By.CSS_SELECTOR, ".artifact-status span, .artifact-status")
        actual_status = status_element.text.lower()
        
        assert actual_status == status.lower(), f"Expected artifact with title '{summary}' to have status '{status}', but got '{actual_status}'"
        log.debug(f"Verified artifact with title '{summary}' has status '{status}'")
        return
        
    except Exception as e:
        log.debug(f"Could not find artifact with title '{summary}': {e}")
    
    raise AssertionError(f"No artifact found with title '{summary}'")
