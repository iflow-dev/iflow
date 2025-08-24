from selenium.webdriver.common.by import By
from radish import step, world

from bdd.controls.artifact import Artifacts
from bdd.controls.editor import Editor
from logging_config import logger


@step("I create a {artifact_type:w}")
@step("I create a new {artifact_type:w}")
def i_create_an_artifact(step, artifact_type):
    """Create a new artifact with the specified type.

    Accept both "I create a requirement" and "I create a new requirement".
    """
    editor = Editor(world.driver)
    logger.trace(f"Editor control created, opening modal for {artifact_type}...")
    editor.open()
    # If the captured artifact_type is the word 'new' (due to pattern ambiguity),
    # try to recover a sensible default: treat it as 'requirement'.
    if artifact_type.lower() == "new":
        resolved_type = "requirement"
        logger.trace("Captured artifact_type='new' — defaulting to 'requirement'")
    else:
        resolved_type = artifact_type
    # Set the type field to the specified artifact type
    editor.set("type", resolved_type)


@step("I create a new requirement with name {name:QuotedString}")
def i_create_a_new_requirement_with_name(step, name):
    editor = Editor(world.driver)
    editor.open()
    # Set the default type to "requirement"
    editor.set("type", "requirement")
    editor.set("summary", name)


@step("I set the {field:w} to {value:QuotedString}")
def i_set_field_to(step, field, value):
    editor = Editor(world.driver)
    editor.set(field, value)


@step("I cancel the artifact creation")
def i_cancel_artifact_creation(step):
    editor = Editor(world.driver)
    editor.cancel()


@step("I see the artifact {identifier:QuotedString}")
def i_see_artifact(step, identifier):
    """Verify that a specific artifact is visible by ID or summary."""
    artifacts = Artifacts()
    
    try:
        # Check if identifier is a numeric string like "00001"
        if identifier.isdigit():
            # Look for artifact with this exact ID string
            artifact_element = artifacts.find_one(id=identifier)
        else:
            # Treat as summary
            artifact_element = artifacts.find_one(summary=identifier)
        
        # Verify the artifact is visible
        assert artifact_element, f"Artifact '{identifier}' not found"
        logger.debug(f"Artifact '{identifier}' is visible")
        
    except (ValueError, AttributeError) as e:
        # Fallback to summary search
        try:
            artifact_element = artifacts.find_one(summary=identifier)
            assert artifact_element, f"Artifact with summary '{identifier}' not found"
            logger.debug(f"Artifact with summary '{identifier}' is visible")
        except Exception:
            raise AssertionError(f"Could not find artifact '{identifier}' by ID or summary")


@step("I do not see the artifact {identifier}")
def i_do_not_see_artifact(step, identifier):
    """Verify that the specified artifact is NOT visible."""
    artifacts = Artifacts()
    
    try:
        if identifier.isdigit():
            # Look for artifact with this exact ID string
            artifact_element = artifacts.find_one(id=identifier)
        else:
            # Treat as summary
            artifact_element = artifacts.find_one(summary=identifier)
        
        # If we found the artifact, it should NOT be visible
        if artifact_element:
            raise AssertionError(f"Artifact '{identifier}' was found but should not be visible")
        
        logger.debug(f"Artifact '{identifier}' correctly not visible")
        
    except ValueError:
        # If find_one raises ValueError, the artifact doesn't exist - that's good
        logger.debug(f"Artifact '{identifier}' correctly not found")
        pass


@step("I search for artifacts with {search_text:QuotedString}")
def i_search_for_artifacts_with(step, search_text):
    # Find the search input field
    search_input = world.driver.find_element(By.ID, "search-input")
    logger.trace("Found search input field")

    # Clear and enter search text
    search_input.clear()
    search_input.send_keys(search_text)
    logger.trace(f"Entered search text: '{search_text}'")

    # Wait for search to complete (if there's a search button, click it)
    try:
        search_button = world.driver.find_element(By.ID, "searchButton")
        search_button.click()
    except Exception:
        # No search button, search might be automatic
        pass


@step("I see {count:d} search results")
def i_see_search_results(step, count):
    """Verify the number of search results after applying a search filter."""
    results = Artifacts().find()
    actual_count = len(results)
    assert actual_count == count, f"Expected {count}, but got {actual_count}"
