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
    editor.locate()
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
    from controls.artifact_control import Artifacts
    from controls.base import ControlBase
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    # Enable debug mode for this test run to handle click interception issues
    ControlBase.enable_debug_for_test()
    
    # Use Artifacts.find_one to locate the artifact
    artifacts = Artifacts()
    artifact_tile = artifacts.find_one(id=artifact_id)
    
    # Find the edit button within the artifact tile
    edit_button = artifact_tile.locate().find_element(By.CSS_SELECTOR, "button[onclick*='openEditModal']")
    
    # Scroll the button into view and ensure it's clickable
    world.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", edit_button)
    
    # Wait for the button to be clickable
    wait = WebDriverWait(world.driver, 10)
    wait.until(EC.element_to_be_clickable(edit_button))
    
    # Try regular click first, fallback to JavaScript click if needed
    try:
        edit_button.click()
        log.debug(f"Opened artifact with ID '{artifact_id}' for editing (regular click)")
    except Exception as e:
        log.debug(f"Regular click failed, trying JavaScript click: {e}")
        world.driver.execute_script("arguments[0].click();", edit_button)
        log.debug(f"Opened artifact with ID '{artifact_id}' for editing (JavaScript click)")

@step("I open the artifact {summary:QuotedString}")
def i_open_artifact_by_summary(step, summary):
    """Open an artifact with the specified title/summary (quotes = title search)."""
    from controls.artifact_control import Artifacts
    from controls.base import ControlBase
    from selenium.webdriver.common.by import By
    
    # Enable debug mode for this test run to handle click interception issues
    ControlBase.enable_debug_for_test()
    
    # Use Artifacts.find_one to locate the artifact
    artifacts = Artifacts()
    artifact_tile = artifacts.find_one(summary=summary)
    
    # Find the edit button within the artifact tile
    edit_button = artifact_tile.locate().find_element(By.CSS_SELECTOR, "button[onclick*='openEditModal']")
    
    # Use enhanced click handling with debug mode
    try:
        edit_button.click()
        log.debug(f"Opened artifact with title '{summary}' for editing (regular click)")
    except Exception as e:
        log.debug(f"Regular click failed, trying JavaScript click: {e}")
        # Use JavaScript click as fallback
        world.driver.execute_script("arguments[0].click();", edit_button)
        log.debug(f"Opened artifact with title '{summary}' for editing (JavaScript click)")

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
    from controls.artifact_control import Artifacts
    from selenium.webdriver.common.by import By
    
    # Use Artifacts.find_one to locate the artifact
    artifacts = Artifacts()
    artifact_tile = artifacts.find_one(id=artifact_id)
    
    # Find the status element within the artifact tile
    status_element = artifact_tile.locate().find_element(By.CSS_SELECTOR, ".artifact-status span, .artifact-status")
    actual_status = status_element.text.lower()
    
    assert actual_status == status.lower(), f"Expected artifact with ID '{artifact_id}' to have status '{status}', but got '{actual_status}'"
    log.debug(f"Verified artifact with ID '{artifact_id}' has status '{status}'")

@step("I see artifact with {summary:QuotedString} has status {status:QuotedString}")
def i_see_artifact_has_status_by_summary(step, summary, status):
    """Verify that the specified artifact (by title) has the expected status."""
    from controls.artifact_control import Artifacts
    from selenium.webdriver.common.by import By
    
    # Use Artifacts.find_one to locate the artifact
    artifacts = Artifacts()
    artifact_tile = artifacts.find_one(summary=summary)
    
    # Find the status element within the artifact tile
    status_element = artifact_tile.locate().find_element(By.CSS_SELECTOR, ".artifact-status span, .artifact-status")
    actual_status = status_element.text.lower()
    
    assert actual_status == status.lower(), f"Expected artifact with title '{summary}' to have status '{status}', but got '{actual_status}'"
    log.debug(f"Verified artifact with title '{summary}' has status '{status}'")
