"""
Step definitions for testing status field default values in the editor.
This module tests that the status field properly shows default values and actual values.
"""

from radish import step, world
from bdd.controls.artifact import Artifacts
from bdd.controls.editor import Editor
from bdd.controls.artifact_tile import ArtifactTile
from bdd.logging import logger


@step("I see the editor is open")
def i_see_editor_is_open(step):
    """Verify that the artifact editor modal is open and visible."""
    editor = Editor(world.driver)
    editor.locate()


@step("I see the status is {expected_status:QuotedString}")
def i_see_status_is(step, expected_status):
    """Verify that the status field shows the expected status value."""
    editor = Editor(world.driver)
    actual_value = editor.status
    assert actual_value == expected_status


@step("I open the artifact #{id:w}")
def i_open_artifact_by_id(step, id):
    """Open an artifact with the specified numeric ID."""
    artifacts = Artifacts()
    artifact_element = artifacts.find_one(id=id)
    tile = ArtifactTile(artifact_element.locate())
    tile.click_edit_button(world.driver)


@step("I open the artifact {title:QuotedString}")
def i_open_artifact_by_title(step, title):
    """Open an artifact with the specified title/summary."""
    artifacts = Artifacts()
    artifact_element = artifacts.find_one(summary=title)
    tile = ArtifactTile(artifact_element.locate())
    tile.click_edit_button(world.driver)


# Note: Step "I set the status to {status:QuotedString}" is already defined in artifact_creation_steps.py

# Note: Step "I save the artifact" is already defined in artifact_steps.py


@step("I see artifact {identifier:w} has status {status:QuotedString}")
def i_see_artifact_has_status(step, identifier, status):
    """Verify that the specified artifact has the expected status."""
    artifacts = Artifacts()
    
    # Try to find by ID first (if it's numeric), then by summary
    try:
        # Check if identifier is a numeric string like "00001"
        if identifier.isdigit():
            # Look for artifact with this exact ID string
            artifact_element = artifacts.find_one(id=identifier)
        else:
            # Treat as summary
            artifact_element = artifacts.find_one(summary=identifier)
    except (ValueError, AttributeError):
        # Fallback to summary search
        artifact_element = artifacts.find_one(summary=identifier)
    
    # Create ArtifactTile control and get status text
    tile = ArtifactTile(artifact_element.locate())
    actual_status = tile.get_status_text()
    assert actual_status == status.lower(), f"Expected artifact '{identifier}' to have status '{status}', but got '{actual_status}'"
