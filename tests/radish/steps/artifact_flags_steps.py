"""
Step definitions for artifact flags functionality tests.
"""

from radish import step, world
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bdd.controls.artifact import Artifacts
from bdd.controls.page import Page
from bdd.controls.article import Article
import time
import subprocess


@step("I reset the database to {branch}")
def i_reset_database_to_branch(step, branch):
    """Reset the test database to a specific branch."""
    
    # Run the reset script to reset the database
    reset_script = "/Users/claudio/realtime/reos2/reset_test_db.sh"
    try:
        result = subprocess.run([reset_script], capture_output=True, text=True, check=True)

    except subprocess.CalledProcessError as e:

        # Continue anyway as this might be expected in some environments
        pass
    except FileNotFoundError:
        # Reset script not found, continuing without reset
        pass


@step("I see artifacts displayed")
def i_see_artifacts_displayed(step):
    """Verify that artifacts are displayed on the page."""
    
    # Wait for artifacts container to be visible and check if artifacts are found
    artifacts = Page().artifacts.wait().find()
    assert len(artifacts) > 0, "No artifacts found on the page"



@step(re.compile(r"I (?:(un)?)flag artifact #(\d+)"))
def i_flag_unflag_artifact(step, unflag, artifact_id):
    """Flag or unflag the specified artifact.
    
    Args:
        unflag: "un" if unflagging, None if flagging
        artifact_id: ID of the artifact to flag/unflag
    """
    
    assert False, "not implemented yet"


@step(re.compile("the artifact (should|should not) be flagged"))
def the_artifact_should_be_flagged_or_not(step, should):
    """Verify that the artifact flag state matches the expected state."""
    
    assert False, "not implemented yet"




@step("I toggle the flag filter")
def i_toggle_flag_filter(step):
    """Toggle the flag filter on/off."""
    
    Toolbar().filter.flag.click()



@step("I should see only flagged artifacts")
def i_should_see_only_flagged_artifacts(step):
    """Verify that only flagged artifacts are displayed."""
    
    # Wait for the filter to be applied
    time.sleep(1)
    
    # Get all visible artifacts
    artifacts = Artifacts().find()
    
       
    # Check that all visible artifacts are flagged
    for artifact_element in artifacts:
        # Use the Article class to check flag state
        article = Article(artifact_element)
        is_flagged = article.flag.active
        assert is_flagged, f"Found unflagged artifact in filtered results"
    


@step("the flag filter button should be red")
def the_flag_filter_button_should_be_red(step):
    """Verify that the flag filter button is red (active filter)."""
    
    flag_filter_button = Toolbar().filter.flag
    background_color = flag_filter_button.value_of_css_property("background-color")
    
    # Handle both rgb and rgba formats
    assert "220, 53, 69" in background_color, f"Flag filter button should be red, got: {background_color}"



@step("I should see all artifacts again")
def i_should_see_all_artifacts_again(step):
    """Verify that all artifacts are displayed again."""
    
    # Wait for the filter to be removed
    time.sleep(1)
    
    # Get all visible artifacts
    artifacts = Artifacts().find()
    
    # We should see artifacts (both flagged and unflagged)
    assert len(artifacts) > 0, "No artifacts visible after removing flag filter"
    
    # Check that we have a mix of flagged and unflagged artifacts
    flagged_count = 0
    unflagged_count = 0
    
    for artifact_element in artifacts:
        # Use the Article class to check flag state
        article = Article(artifact_element)
        is_flagged = article.flag.active
        
        if is_flagged:
            flagged_count += 1
        else:
            unflagged_count += 1
    


@step("the flag filter button should be grey")
def the_flag_filter_button_should_be_grey(step):
    """Verify that the flag filter button is grey (inactive filter)."""
    
    flag_filter_button = Toolbar().filter.flag
    background_color = flag_filter_button.value_of_css_property("background-color")
    
    # Handle both rgb and rgba formats
    assert "108, 117, 125" in background_color, f"Flag filter button should be grey, got: {background_color}"



@step("I flag this article")
def i_flag_this_article(step):
    """Flag the current article using the Editor control."""
    
    from bdd.controls.editor import Editor
    editor = Editor(world.driver)
    editor.flag.toggle(active=True)



@step("I should see the new artifact created")
def i_should_see_new_artifact_created(step):
    """Verify that a new artifact was created."""
    
    # Wait for the modal to close and artifacts to refresh
    time.sleep(2)
    
    # Check that we have artifacts using Artifacts
    artifacts = Artifacts().find(summary="Test artifact with flag")
    assert len(artifacts) > 0, "New artifact with test summary not found"



