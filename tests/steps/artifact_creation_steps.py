from radish import given, when, then, step
from controls.artifact_control import Artifact, Artifacts
import logging

# Set up logging
log = logging.getLogger(__name__)

@step("I create a new requirement")
def i_create_a_new_requirement(step):
    """Create a new requirement artifact."""
    from radish import world
    
    log.trace("Starting: I create a new requirement")
    
    try:
        from controls.editor import Editor
        editor = Editor(world.driver)
        log.trace("Editor control created, opening modal...")
        editor.open()
        
    except Exception as e:
        log.debug(f"Failed to open artifact creation modal: {e}")
        raise AssertionError(f"Failed to open artifact creation modal: {e}")

@step("I create a new requirement with name {name:QuotedString}")
def i_create_a_new_requirement_with_name(step, name):
    """Create a new requirement artifact with a specific name."""
    from radish import world
    
    log.trace("Starting: I create a new requirement with name")
    
    try:
        from controls.editor import Editor
        editor = Editor(world.driver)
        editor.open()
        
        # Set the summary to the provided name
        editor.set_summary(name)
        
    except Exception as e:
        log.debug(f"Failed to create requirement with name '{name}': {e}")
        raise AssertionError(f"Failed to create requirement with name '{name}': {e}")

@step("I see the artifact creation form")
def i_see_artifact_creation_form(step):
    """Verify that the artifact creation form is displayed."""
    from radish import world
    
    log.trace("Verifying artifact creation form is displayed")
    
    try:
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        # Wait for the modal to be visible
        wait = WebDriverWait(world.driver, 10)
        modal = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "modal-content")))
        
        # Verify the modal contains form elements
        form_elements = modal.find_elements(By.TAG_NAME, "input")
        assert len(form_elements) > 0, "No form elements found in modal"
        
    except Exception as e:
        log.debug(f"Failed to verify artifact creation form: {e}")
        raise AssertionError(f"Failed to verify artifact creation form: {e}")

@step("I set the type to {type_value:QuotedString}")
def i_set_type_to(step, type_value):
    """Set the artifact type to the specified value."""
    from radish import world
    
    log.trace(f"Setting artifact type to '{type_value}'")
    
    try:
        from controls.editor import Editor
        editor = Editor(world.driver)
        editor.set_type(type_value)
        
    except Exception as e:
        log.debug(f"Failed to set artifact type to '{type_value}': {e}")
        raise AssertionError(f"Failed to set artifact type to '{type_value}': {e}")

@step("I set the summary to {summary:QuotedString}")
def i_set_summary_to(step, summary):
    """Set the artifact summary to the specified value."""
    from radish import world
    
    log.trace(f"Setting artifact summary to '{summary}'")
    
    try:
        from controls.editor import Editor
        editor = Editor(world.driver)
        editor.set_summary(summary)
        
    except Exception as e:
        log.debug(f"Failed to set artifact summary to '{summary}': {e}")
        raise AssertionError(f"Failed to set artifact summary to '{summary}': {e}")

@step("I set the description to {description:QuotedString}")
def i_set_description_to(step, description):
    """Set the artifact description to the specified value."""
    from radish import world
    
    log.trace(f"Setting artifact description to '{description}'")
    
    try:
        from controls.editor import Editor
        editor = Editor(world.driver)
        editor.set_description(description)
        
    except Exception as e:
        log.debug(f"Failed to set artifact description to '{description}': {e}")
        raise AssertionError(f"Failed to set artifact description to '{description}': {e}")

@step("I set the status to {status:QuotedString}")
def i_set_status_to(step, status):
    """Set the artifact status to the specified value."""
    from radish import world
    
    log.trace(f"Setting artifact status to '{status}'")
    
    try:
        from controls.editor import Editor
        editor = Editor(world.driver)
        editor.set_status(status)
        
    except Exception as e:
        log.debug(f"Failed to set artifact status to '{status}': {e}")
        raise AssertionError(f"Failed to set artifact status to '{status}': {e}")

@step("I see the new artifact in the list")
def i_see_new_artifact_in_list(step):
    """Verify that the new artifact appears in the list."""
    from radish import world
    
    log.trace("Verifying new artifact appears in list")
    
    try:
        # Use the new Artifact class to find the artifact
        artifact = Artifact(summary="Test requirement for BDD testing")
        
        # Check if the artifact exists within 5 seconds
        if artifact.exists(5):
            log.trace("Found artifact with summary: Test requirement for BDD testing")
        else:
            raise AssertionError("New artifact not found in list")
        
    except Exception as e:
        log.debug(f"Failed to verify new artifact in list: {e}")
        raise AssertionError(f"Failed to verify new artifact in list: {e}")

@step("I cancel the artifact creation")
def i_cancel_artifact_creation(step):
    """Cancel the artifact creation."""
    from radish import world
    
    log.trace("Canceling artifact creation...")
    
    try:
        from controls.editor import Editor
        editor = Editor(world.driver)
        editor.cancel()
        
    except Exception as e:
        log.debug(f"Failed to cancel artifact creation: {e}")
        raise AssertionError(f"Failed to cancel artifact creation: {e}")

@step("I remain on the search view")
def i_remain_on_search_view(step):
    """Verify that we remain on the search view after cancellation."""
    from radish import world
    
    log.trace("Verifying we remain on search view after cancellation")
    
    try:
        # Check that we're still on the home page (search view)
        from selenium.webdriver.common.by import By
        search_input = world.driver.find_element(By.ID, "searchInput")
        assert search_input.is_displayed(), "Search input not visible - not on search view"
        
    except Exception as e:
        log.debug(f"Failed to verify we remain on search view: {e}")
        raise AssertionError(f"Failed to verify we remain on search view: {e}")

@step("I search for artifacts with {search_text:QuotedString}")
def i_search_for_artifacts_with(step, search_text):
    """Search for artifacts with the specified text."""
    from radish import world
    
    log.trace(f"Searching for artifacts with text: '{search_text}'")
    
    try:
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        # Find the search input field
        search_input = world.driver.find_element(By.ID, "searchInput")
        log.trace("Found search input field")
        
        # Clear and enter search text
        search_input.clear()
        search_input.send_keys(search_text)
        log.trace(f"Entered search text: '{search_text}'")
        
        # Wait for search to complete (if there's a search button, click it)
        try:
            search_button = world.driver.find_element(By.ID, "searchButton")
            search_button.click()
        except:
            # No search button, search might be automatic
            pass
        
    except Exception as e:
        log.debug(f"Failed to search for artifacts: {e}")
        raise AssertionError(f"Failed to search for artifacts: {e}")

@step("I see {count:d} search results")
def i_see_search_results(step, count):
    """Verify that the search returns the specified number of results."""
    from radish import world
    
    log.trace(f"Verifying search returns {count} results")
    
    try:
        # Use Artifacts to count results
        from controls.artifact_control import Artifacts
        artifacts = Artifacts(world.driver).find()
        actual_count = len(artifacts)
        
        assert actual_count == count, f"Expected {count} search results, but got {actual_count}"
        
    except Exception as e:
        log.debug(f"Failed to verify search results: {e}")
        raise AssertionError(f"Failed to verify search results: {e}")


