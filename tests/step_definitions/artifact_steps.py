"""
Step definitions for artifact management BDD tests.
This file contains the Python implementation of the Gherkin steps.
"""

from radish import given, when, then, step
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time

class ArtifactTestWorld:
    """World object to share state between steps."""
    
    def __init__(self):
        self.driver = None
        self.current_artifact_id = None
        self.filter_state = {}
        self.wait = None

@step("I am on the artifacts page")
def i_am_on_artifacts_page(step):
    """Navigate to the artifacts page."""
    world = step.context.world
    world.driver.get("http://localhost:8080")
    world.wait = WebDriverWait(world.driver, 10)
    
    # Wait for the page to load
    world.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "artifacts-container")))

@step("I am logged in as a user")
def i_am_logged_in_as_user(step):
    """Verify user is logged in (assuming no authentication required for demo)."""
    pass

@step("I click the \"{button_text}\" button")
def i_click_button(step, button_text):
    """Click a button with the specified text."""
    world = step.context.world
    button = world.driver.find_element(By.XPATH, f"//button[contains(text(), '{button_text}')]")
    button.click()

@step("I fill in the artifact details")
def i_fill_in_artifact_details(step):
    """Fill in the artifact form with the data table."""
    world = step.context.world
    
    # Wait for modal to appear
    world.wait.until(EC.visibility_of_element_located((By.ID, "artifactModal")))
    
    # Get the data table from the step
    data = step.table
    
    for row in data:
        field = row[0]
        value = row[1]
        
        if field == "Type":
            select = Select(world.driver.find_element(By.ID, "artifactType"))
            select.select_by_value(value)
        elif field == "Summary":
            world.driver.find_element(By.ID, "artifactSummary").send_keys(value)
        elif field == "Description":
            world.driver.find_element(By.ID, "artifactDescription").send_keys(value)
        elif field == "Category":
            world.driver.find_element(By.ID, "artifactCategory").send_keys(value)
        elif field == "Status":
            select = Select(world.driver.find_element(By.ID, "artifactStatus"))
            select.select_by_value(value)

@step("I click \"{button_text}\"")
def i_click_save_artifact(step, button_text):
    """Click the save artifact button."""
    world = step.context.world
    save_button = world.driver.find_element(By.XPATH, f"//button[text()='{button_text}']")
    save_button.click()

@step("a new artifact should be created")
def new_artifact_should_be_created(step):
    """Verify that a new artifact was created."""
    world = step.context.world
    
    # Wait for modal to close
    world.wait.until(EC.invisibility_of_element_located((By.ID, "artifactModal")))
    
    # Verify the artifact appears in the list
    artifacts = world.driver.find_elements(By.CLASS_NAME, "artifact-card")
    assert len(artifacts) > 0, "No artifacts found after creation"

@step("it should appear in the artifacts list")
def artifact_should_appear_in_list(step):
    """Verify the artifact appears in the artifacts list."""
    world = step.context.world
    
    # Look for the artifact with the test summary
    artifact = world.driver.find_element(By.XPATH, "//div[contains(@class, 'artifact-summary') and contains(text(), 'Test requirement')]")
    assert artifact.is_displayed(), "New artifact not found in the list"

@step("the modal should close")
def modal_should_close(step):
    """Verify the modal dialog closes after saving."""
    world = step.context.world
    
    # Wait for modal to be hidden
    world.wait.until(EC.invisibility_of_element_located((By.ID, "artifactModal")))
