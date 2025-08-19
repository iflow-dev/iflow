"""
Step definitions for status onliner functionality.
Tests that status is displayed as a one-liner text in artifact tiles.
"""

from radish import step, world
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@step("I am on the artifacts view")
def i_am_on_artifacts_view(step):
    """Navigate to the artifacts view."""
    from radish import world
    
    # Navigate to the base URL which should show the artifacts view
    world.driver.get(world.base_url)
    
    # Wait for the page to load
    wait = WebDriverWait(world.driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, "artifacts-container")))

@step("I have artifacts with different statuses")
def i_have_artifacts_with_different_statuses(step):
    """Ensure we have artifacts with different statuses to test."""
    from radish import world
    
    # Wait for artifacts to load
    wait = WebDriverWait(world.driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "artifact-card")))
    
    # Check that we have multiple artifacts
    artifacts = world.driver.find_elements(By.CLASS_NAME, "artifact-card")
    assert len(artifacts) > 0, "No artifacts found"

@step("I view an artifact tile")
def i_view_an_artifact_tile(step):
    """View an artifact tile to check its content."""
    from radish import world
    
    # Wait for artifacts to be visible
    wait = WebDriverWait(world.driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "artifact-card")))
    
    # Get the first artifact tile
    artifacts = world.driver.find_elements(By.CLASS_NAME, "artifact-card")
    assert len(artifacts) > 0, "No artifacts found"
    
    # Store the first artifact for verification
    world.current_artifact = artifacts[0]

@step("I should see the status displayed as a one-liner text")
def i_should_see_status_as_one_liner_text(step):
    """Verify that status is displayed as a one-liner text."""
    from radish import world
    
    # Look for the status onliner in the artifact content
    status_onliner = world.current_artifact.find_element(By.CLASS_NAME, "status-onliner")
    assert status_onliner.is_displayed(), "Status onliner is not visible"
    
    # Check that it contains text
    status_text = status_onliner.text.strip()
    assert status_text, "Status onliner text is empty"

@step("the status text should be clearly visible in the tile content")
def status_text_should_be_clearly_visible(step):
    """Verify that the status text is clearly visible in the tile content."""
    from radish import world
    
    # Check that the status onliner is in the content area, not just the header
    status_onliner = world.current_artifact.find_element(By.CLASS_NAME, "status-onliner")
    
    # Verify it's positioned in the content area
    content_area = world.current_artifact.find_element(By.CLASS_NAME, "artifact-content")
    assert status_onliner in content_area.find_elements(By.CLASS_NAME, "status-onliner"), \
        "Status onliner should be in the content area"

@step("I have an artifact with status {status:QuotedString}")
def i_have_artifact_with_status(step, status):
    """Ensure we have an artifact with the specified status."""
    from radish import world
    
    # Wait for artifacts to load
    wait = WebDriverWait(world.driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "artifact-card")))
    
    # Find an artifact with the specified status
    artifacts = world.driver.find_elements(By.CLASS_NAME, "artifact-card")
    
    for artifact in artifacts:
        try:
            # Check the status header first
            status_header = artifact.find_element(By.CLASS_NAME, "artifact-status")
            if status.lower() in status_header.text.lower():
                world.current_artifact = artifact
                return
        except:
            continue
    
    # If no artifact found with the status, we'll use the first one and update it
    world.current_artifact = artifacts[0]

@step("I should see {status:QuotedString} displayed as a one-liner text")
def i_should_see_status_displayed_as_one_liner(step, status):
    """Verify that the specific status is displayed as a one-liner text."""
    from radish import world
    
    # Look for the status onliner
    status_onliner = world.current_artifact.find_element(By.CLASS_NAME, "status-onliner")
    assert status_onliner.is_displayed(), "Status onliner is not visible"
    
    # Check that it contains the expected status
    status_text = status_onliner.text.strip()
    assert status.lower() in status_text.lower(), \
        f"Expected status '{status}' not found in onliner text: '{status_text}'"

@step("the status onliner should be separate from the status header")
def status_onliner_should_be_separate_from_header(step):
    """Verify that the status onliner is separate from the status header."""
    from radish import world
    
    # Check that we have both a status header and a status onliner
    status_header = world.current_artifact.find_element(By.CLASS_NAME, "artifact-status")
    status_onliner = world.current_artifact.find_element(By.CLASS_NAME, "status-onliner")
    
    # They should be different elements
    assert status_header != status_onliner, "Status onliner should be different from status header"
    
    # They should be in different areas of the tile
    header_area = world.current_artifact.find_element(By.CLASS_NAME, "artifact-header")
    content_area = world.current_artifact.find_element(By.CLASS_NAME, "artifact-content")
    
    assert status_header in header_area.find_elements(By.CLASS_NAME, "artifact-status"), \
        "Status header should be in header area"
    assert status_onliner in content_area.find_elements(By.CLASS_NAME, "status-onliner"), \
        "Status onliner should be in content area"

@step("I change the artifact status to {new_status:QuotedString}")
def i_change_artifact_status_to(step, new_status):
    """Change the artifact status to the specified value."""
    from radish import world
    
    # Click the edit button for the current artifact
    edit_button = world.current_artifact.find_element(By.CSS_SELECTOR, "button[onclick*='openEditModal']")
    edit_button.click()
    
    # Wait for modal to open
    wait = WebDriverWait(world.driver, 10)
    wait.until(EC.visibility_of_element_located((By.ID, "artifactModal")))
    
    # Select the new status
    status_select = world.driver.find_element(By.ID, "artifactStatus")
    from selenium.webdriver.support.ui import Select
    select = Select(status_select)
    select.select_by_value(new_status.lower().replace(" ", "_"))
    
    # Save the changes
    save_button = world.driver.find_element(By.ID, "submitButton")
    save_button.click()
    
    # Wait for modal to close and page to refresh
    wait.until(EC.invisibility_of_element_located((By.ID, "artifactModal")))
    time.sleep(1)  # Allow time for the page to refresh

@step("the status onliner should display {expected_status:QuotedString}")
def status_onliner_should_display(step, expected_status):
    """Verify that the status onliner displays the expected status."""
    from radish import world
    
    # Wait for the page to refresh and find the updated artifact
    wait = WebDriverWait(world.driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "artifact-card")))
    
    # Find the artifact with the same ID (we'll need to get the ID from the current artifact)
    # For now, let's check the first artifact's status onliner
    artifacts = world.driver.find_elements(By.CLASS_NAME, "artifact-card")
    status_onliner = artifacts[0].find_element(By.CLASS_NAME, "status-onliner")
    
    # Check that it contains the expected status
    status_text = status_onliner.text.strip()
    assert expected_status.lower() in status_text.lower(), \
        f"Expected status '{expected_status}' not found in onliner text: '{status_text}'"

@step("the change should be immediately visible")
def change_should_be_immediately_visible(step):
    """Verify that the status change is immediately visible."""
    from radish import world
    
    # The status onliner should be visible and updated
    artifacts = world.driver.find_elements(By.CLASS_NAME, "artifact-card")
    status_onliner = artifacts[0].find_element(By.CLASS_NAME, "status-onliner")
    
    assert status_onliner.is_displayed(), "Status onliner should be visible after update"
    assert status_onliner.text.strip(), "Status onliner should have text after update"
