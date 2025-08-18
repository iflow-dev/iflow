"""
Step definitions for toolbar refresh functionality testing.
"""

from radish import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from controls import Button

@when("I click the refresh button in the toolbar")
def i_click_refresh_button_in_toolbar(step):
    """Click the refresh button in the toolbar."""
    from radish import world
    
    # Find the refresh button by its icon
    refresh_button = Button("refresh button", "//button[.//ion-icon[@name='refresh-outline']]")
    refresh_button.click(world.driver)
    
    # Wait a moment for the refresh to complete
    import time
    time.sleep(1)

@then("the artifacts list should be refreshed")
def artifacts_list_should_be_refreshed(step):
    """Verify that the artifacts list has been refreshed."""
    from radish import world
    
    # Wait for the artifacts container to be present
    wait = WebDriverWait(world.driver, 10)
    artifacts_container = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "artifacts-container"))
    )
    
    # Verify that the container is not showing loading state
    loading_elements = artifacts_container.find_elements(By.CLASS_NAME, "loading")
    assert len(loading_elements) == 0, "Artifacts container is still in loading state"

@then("I should see the latest artifacts data")
def i_should_see_latest_artifacts_data(step):
    """Verify that the latest artifacts data is displayed."""
    from radish import world
    
    # Wait for artifacts to be loaded
    wait = WebDriverWait(world.driver, 10)
    artifact_cards = wait.until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "artifact-card"))
    )
    
    # Verify that artifacts are displayed
    assert len(artifact_cards) > 0, "No artifacts are displayed after refresh"
    
    # Verify that the artifacts container is not empty
    artifacts_container = world.driver.find_element(By.CLASS_NAME, "artifacts-container")
    assert artifacts_container.text.strip() != "", "Artifacts container is empty after refresh"
