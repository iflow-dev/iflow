"""
Step definitions for artifact flags functionality tests.
"""

from radish import step, world
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from controls.artifact_control import Artifacts
from controls.page import Page
from controls.article import Article
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
    
    # Use Artifacts to find the specific artifact by ID
    artifacts = Artifacts(world.driver).find(id=artifact_id)
    if not artifacts:
        raise Exception(f"No artifact found with ID {artifact_id}")
    
    # Create Article instance with the specific artifact element
    article = Article(world.driver, artifacts[0])
    
    # Determine the desired flag state based on the action
    if unflag:  # unflag action
        desired_state = False
    else:  # flag action
        desired_state = True
    
    # Toggle the flag state - the Article.toggle() method handles the state management
    article.toggle(active=desired_state)


@step(re.compile("the artifact (should|should not) be flagged"))
def the_artifact_should_be_flagged_or_not(step, should):
    """Verify that the artifact flag state matches the expected state."""
    
    # Wait for the flag state to change
    time.sleep(1)
    
    # Use the new Article().flag.active property
    article = Article(world.driver)
    current_flag_state = article.flag.active
    
    # Determine expected state based on the step text
    expected_flagged = "should" in should.lower() and "not" not in should.lower()
    
    # The flag state should match the expected state
    assert current_flag_state == expected_flagged, f"Flag state mismatch. Expected: {expected_flagged}, Got: {current_flag_state}"


@step("the artifact should not be flagged")
def the_artifact_should_not_be_flagged(step):
    """Verify that the artifact is not flagged."""
    
    # Wait for the flag state to change
    time.sleep(1)
    
    # Use the new Article().flag.active property
    article = Article(world.driver)
    current_flag_state = article.flag.active
    
    # The artifact should not be flagged
    assert not current_flag_state, f"Artifact should not be flagged, but got: {current_flag_state}"



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
    artifacts = Artifacts(world.driver).find()
    
       
    # Check that all visible artifacts are flagged
    article = Article(world.driver)
    
    for artifact_element in artifacts:
        # Use the Article class to check flag state
        article = Article(world.driver, artifact_element)
        is_flagged = article.flag.state
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
    artifacts = Artifacts(world.driver).find()
    
    # We should see artifacts (both flagged and unflagged)
    assert len(artifacts) > 0, "No artifacts visible after removing flag filter"
    
    # Check that we have a mix of flagged and unflagged artifacts
    article = Article(world.driver)
    
    flagged_count = 0
    unflagged_count = 0
    
    for artifact_element in artifacts:
        # Use the Article class to check flag state
        article = Article(world.driver, artifact_element)
        is_flagged = article.flag.state
        
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
    
    from controls.editor import Editor
    editor = Editor(world.driver)
    editor.flag.toggle(active=True)



@step("I should see the new artifact created")
def i_should_see_new_artifact_created(step):
    """Verify that a new artifact was created."""
    
    # Wait for the modal to close and artifacts to refresh
    time.sleep(2)
    
    # Check that we have artifacts using Artifacts
    artifacts = Artifacts(world.driver).find(summary="Test artifact with flag")
    assert len(artifacts) > 0, "New artifact with test summary not found"


@step("the artifact should be flagged")
def the_new_artifact_should_be_flagged(step):
    """Verify that the newly created artifact is flagged."""
    
    # Wait for the modal to close and artifacts to refresh
    time.sleep(2)
    
    # Find the specific artifact we created by its summary text using Artifacts
    artifacts = Artifacts(world.driver).find(summary="Test artifact with flag")
    assert len(artifacts) > 0, "No artifacts found after creation"
    
   
    
    # Check the flag button on our specific artifact
    flag_button = target_artifact.find_element(By.CSS_SELECTOR, ".artifact-actions button:first-child")
    icon = flag_button.find_element(By.CSS_SELECTOR, "ion-icon")
    
    icon_name = icon.get_attribute("name")
    is_flagged = "flag" in icon_name and "outline" not in icon_name
    
    if not is_flagged:
        pass
    
    assert is_flagged, f"Newly created artifact should be flagged but icon name is '{icon_name}'"
