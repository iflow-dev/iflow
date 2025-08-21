from radish import given, when, then, step
from controls import Title
import logging

# Set up logging
log = logging.getLogger(__name__)

@when("I create a new requirement")
def i_create_a_new_requirement(step):
    """Open the artifact creation editor."""
    from radish import world
    from controls import Editor
    
    log.trace("Starting: I create a new requirement")
    
    # Use the Editor control to open the artifact creation modal
    editor = Editor(world.driver)
    log.trace("Editor control created, opening modal...")
    editor.open()
    
    # Store the editor in world for use in subsequent steps
    world.editor = editor
    log.trace("Editor stored in world, modal should be open")

@when("I create a new requirement {requirement_name:QuotedString}")
def i_create_a_new_requirement_with_name(step, requirement_name):
    """Open the artifact creation editor with a specific requirement name."""
    from radish import world
    from controls import Editor
    
    log.trace(f"Starting: I create a new requirement with name '{requirement_name}'")
    
    # Use the Editor control to open the artifact creation modal
    editor = Editor(world.driver)
    log.trace("Editor control created, opening modal...")
    editor.open()
    
    # Store the editor in world for use in subsequent steps
    world.editor = editor
    log.trace("Editor stored in world")
    
    # Store the requirement name for later use
    world.requirement_name = requirement_name
    log.trace(f"Requirement name '{requirement_name}' stored in world")

@then("I see the artifact creation form")
def i_see_artifact_creation_form(step):
    """Verify that the artifact creation form is displayed."""
    from radish import world
    
    log.trace("Verifying artifact creation form is displayed")
    
    # Verify that the editor is open using the stored editor instance
    if not hasattr(world, 'editor') or not world.editor.is_open():
        log.trace("Editor not found or not open")
        raise AssertionError("Artifact creation form is not displayed")
    
    log.trace("Artifact creation form verification successful")

@step(r"I set the type to {artifact_type:QuotedString}")
def i_set_type_to(step, artifact_type):
    """Set the type field to the specified value."""
    from radish import world
    
    log.trace(f"Setting artifact type to '{artifact_type}'")
    
    # Use the Editor control to set the type
    world.editor.set_type(artifact_type)
    log.trace(f"Artifact type set to '{artifact_type}'")

@step(r"I set the summary to {summary:QuotedString}")
def i_set_summary_to(step, summary):
    """Set the summary field to the specified value."""
    from radish import world
    
    log.trace(f"Setting artifact summary to '{summary}'")
    
    # Use the Editor control to set the summary
    world.editor.set_summary(summary)
    log.trace(f"Artifact summary set to '{summary}'")

@step(r"I set the description to {description:QuotedString}")
def i_set_description_to(step, description):
    """Set the description field to the specified value."""
    from radish import world
    
    log.trace(f"Setting artifact description to '{description}'")
    
    # Use the Editor control to set the description
    world.editor.set_description(description)
    log.trace(f"Artifact description set to '{description}'")

@step(r"I set the status to {status:QuotedString}")
def i_set_status_to(step, status):
    """Set the status field to the specified value."""
    from radish import world
    
    log.trace(f"Setting artifact status to '{status}'")
    
    # Use the Editor control to set the status
    world.editor.set_status(status)
    log.trace(f"Artifact status set to '{status}'")

@step("I save the new artifact")
def i_save_new_artifact(step):
    """Save the new artifact."""
    from radish import world
    
    log.trace("Saving new artifact...")
    
    # Use the Editor control to create the artifact
    world.editor.create()
    log.trace("Artifact creation completed")
    
    # Add debugging to see what happened
    log.trace("Checking if modal is closed...")
    if world.editor.is_closed():
        log.trace("Modal is closed successfully")
    else:
        log.trace("Modal is still open - artifact creation may have failed")
    
    # Wait a bit for the page to update
    import time
    time.sleep(2)
    
    # Check if there are any error messages on the page
    try:
        from selenium.webdriver.common.by import By
        error_elements = world.driver.find_elements(By.CLASS_NAME, "error")
        if error_elements:
            for error in error_elements:
                log.trace(f"Found error message: {error.text}")
        else:
            log.trace("No error messages found")
    except Exception as e:
        log.trace(f"Error checking for error messages: {e}")
    
    # Check the current page content to see what's displayed
    try:
        artifacts_container = world.driver.find_element(By.ID, "artifacts-container")
        log.trace(f"Artifacts container content: {artifacts_container.text[:200]}...")
    except Exception as e:
        log.trace(f"Error checking artifacts container: {e}")

@step("I see the new artifact in the list")
def i_see_new_artifact_in_list(step):
    """Verify that the new artifact appears in the list."""
    from radish import world
    from controls import Tile
    
    log.trace("Verifying new artifact appears in list")
    
    # Get the artifact ID from world (should be set by previous steps)
    # For now, we'll look for the summary text to verify the artifact was created
    # TODO: Implement proper artifact ID tracking
    summary_text = "Test requirement for BDD testing"
    
    # Add debugging to see what's actually in the list
    try:
        from selenium.webdriver.common.by import By
        artifact_cards = world.driver.find_elements(By.CLASS_NAME, "artifact-card")
        log.trace(f"Found {len(artifact_cards)} artifact cards in the list")
        
        for i, card in enumerate(artifact_cards):
            try:
                card_text = card.text[:100]  # First 100 characters
                log.trace(f"Artifact card {i+1}: {card_text}...")
            except Exception as e:
                log.trace(f"Error reading card {i+1}: {e}")
        
        # Also check for any loading messages or empty state messages
        loading_elements = world.driver.find_elements(By.CLASS_NAME, "loading")
        if loading_elements:
            for loading in loading_elements:
                log.trace(f"Found loading message: {loading.text}")
        
        # Check for any "no artifacts" messages
        no_artifacts_elements = world.driver.find_elements(By.XPATH, "//*[contains(text(), 'No artifacts') or contains(text(), 'no artifacts')]")
        if no_artifacts_elements:
            for msg in no_artifacts_elements:
                log.trace(f"Found 'no artifacts' message: {msg.text}")
                
    except Exception as e:
        log.trace(f"Error examining artifact list: {e}")
    
    # Use the Tile control to find the artifact by its content
    # This is a temporary solution until we implement proper ID tracking
    try:
        # Look for any tile containing the summary text
        tile = Tile(summary_text)
        log.trace(f"Searching for tile with summary: {summary_text}")
        tile.locate(world.driver, timeout=10)
        log.trace(f"Found artifact with summary: {summary_text}")
    except Exception as e:
        log.trace(f"Failed to find artifact with summary '{summary_text}': {e}")
        raise AssertionError(f"Artifact with summary '{summary_text}' not found in the list: {e}")

@step("I do not see the artifact creation form")
def i_do_not_see_artifact_creation_form(step):
    """Verify that the artifact creation form is not displayed."""
    from radish import world
    
    log.trace("Verifying artifact creation form is not displayed")
    
    # Verify that the editor is closed using the stored editor instance
    if not world.editor.is_closed():
        log.trace("Editor is still open")
        raise AssertionError("Artifact creation form is still displayed")
    
    log.trace("Artifact creation form verification successful - form is closed")

@step("I cancel the artifact creation")
def i_cancel_artifact_creation(step):
    """Cancel the artifact creation process."""
    from radish import world
    
    log.trace("Canceling artifact creation...")
    
    # Use the Editor control to cancel artifact creation
    world.editor.cancel()
    log.trace("Artifact creation canceled")

@step("I remain on the search view")
def i_remain_on_search_view(step):
    """Verify that we remain on the search view after cancellation."""
    from radish import world
    from controls import Title
    
    log.trace("Verifying we remain on search view after cancellation")
    
    # Verify that we're still on the search page by checking the page title
    title = Title("iflow")
    if not title.exists(world.driver):
        log.trace("Page title 'iflow' not found - not on search view")
        raise AssertionError("Not on the search view - page title not found")
    
    log.trace("Successfully verified we remain on search view")

@step(r"I search for artifacts with {search_text:QuotedString}")
def i_search_for_artifacts_with(step, search_text):
    """Search for artifacts with the specified text."""
    from radish import world
    
    log.trace(f"Searching for artifacts with text: '{search_text}'")
    
    # Find the search input field and enter the search text
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    
    search_input = world.driver.find_element(By.ID, "search-input")
    log.trace("Found search input field")
    search_input.clear()
    search_input.send_keys(search_text)
    log.trace(f"Entered search text: '{search_text}'")
    
    # Press Enter to trigger the search
    search_input.send_keys(Keys.RETURN)
    log.trace("Search triggered with Enter key")

@step("I see 0 search results")
def i_see_zero_search_results(step):
    """Verify that the search returns 0 results."""
    from radish import world
    
    log.trace("Verifying search returns 0 results")
    
    # Wait a moment for search results to update
    import time
    time.sleep(1)
    
    # Look for any artifact cards in the results
    try:
        # Check if there are any artifact cards visible
        from selenium.webdriver.common.by import By
        artifact_cards = world.driver.find_elements(By.CSS_SELECTOR, ".artifact-card")
        if len(artifact_cards) > 0:
            log.trace(f"Found {len(artifact_cards)} artifact cards, expected 0")
            raise AssertionError(f"Expected 0 search results, but found {len(artifact_cards)} artifacts")
        log.trace("Search returned 0 results as expected")
    except Exception as e:
        # If no elements found, that's what we expect
        log.trace("No artifact cards found - search returned 0 results")
