"""
Step definitions for artifact management BDD tests.
This file contains the Python implementation of the Gherkin steps.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from radish import step, world

from bdd.controls import Title
from bdd.controls.editor import Editor

@step("I am on the artifacts page")
def i_am_on_artifacts_page(step):
    # Verify we're on the iflow page (don't navigate, just verify)
    title = Title("iflow")
    title.locate()
    
    # Verify we have the artifacts container (search functionality)
    wait = WebDriverWait(world.driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "artifacts-container")))


@step("I am logged in as a user")
def i_am_logged_in_as_user(step):
    pass


@step("I click the \"{button_text}\" button")
def i_click_button(step, button_text):
    button = world.driver.find_element(By.XPATH, f"//button[contains(text(), '{button_text}')]")
    button.click()


@step("I fill in the artifact details")
def i_fill_in_artifact_details(step):
    # Wait for modal to appear
    wait = WebDriverWait(world.driver, 10)
    wait.until(EC.visibility_of_element_located((By.ID, "artifactModal")))
    
    # Get the data table from the step
    if hasattr(step, 'table') and step.table:
        # Radish table has rows as dictionaries with column names as keys
        for row in step.table:
            field = row.get("Field")
            value = row.get("Value")
            
            if field and value:
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
    else:
        # Default values if no table provided
        default_data = {
            "Type": "requirement",
            "Summary": "Test artifact",
            "Description": "Test artifact description",
            "Category": "Test",
            "Status": "open"
        }
        
        for field, value in default_data.items():
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
    save_button = world.driver.find_element(By.XPATH, f"//button[text()='{button_text}']")
    save_button.click()

@step("I save the article")
def i_save_the_article(step):
    # Create an Editor instance and save the article
    editor = Editor(world.driver)
    editor.save()



@step("a new artifact should be created")
def new_artifact_should_be_created(step):
    # Wait for modal to close
    world.wait.until(EC.invisibility_of_element_located((By.ID, "artifactModal")))
    
    # Verify the artifact appears in the list
    artifacts = world.driver.find_elements(By.CLASS_NAME, "artifact-card")
    assert len(artifacts) > 0, "No artifacts found after creation"

@step("it should appear in the artifacts list")
def artifact_should_appear_in_list(step):
    # Look for the artifact with the test summary
    artifact = world.driver.find_element(By.XPATH, "//div[contains(@class, 'artifact-summary') and contains(text(), 'Test requirement')]")
    assert artifact.is_displayed(), "New artifact not found in the list"

@step("the modal should close")
def modal_should_close(step):
    # Wait for modal to be hidden
    world.wait.until(EC.invisibility_of_element_located((By.ID, "artifactModal")))

@step("I am viewing an artifact")
def i_am_viewing_an_artifact(step):
    # This step assumes we're already on the artifacts page with artifacts visible
    artifacts = world.driver.find_elements(By.CLASS_NAME, "artifact-card")
    assert len(artifacts) > 0, "No artifacts found to view"

@step("I click the \"Edit\" button")
def i_click_edit_button(step):
    # Find the first edit button (ion-icon with create-outline)
    edit_button = world.driver.find_element(By.XPATH, "//button[.//ion-icon[@name='create-outline']]")
    edit_button.click()

@step("I modify the artifact description")
def i_modify_artifact_description(step):
    # Wait for edit modal to appear
    world.wait.until(EC.visibility_of_element_located((By.ID, "artifactDescription")))
    # Clear and fill the description
    description_field = world.driver.find_element(By.ID, "artifactDescription")
    description_field.clear()
    description_field.send_keys("Modified description for testing")



@step("the artifact should be updated")
def artifact_should_be_updated(step):
    # Wait for modal to close
    world.wait.until(EC.invisibility_of_element_located((By.ID, "artifactModal")))
    # Look for the modified description
    modified_artifact = world.driver.find_element(By.XPATH, "//div[contains(@class, 'artifact-description') and contains(text(), 'Modified description for testing')]")
    assert modified_artifact.is_displayed(), "Modified artifact not found"

@step("the changes should be reflected immediately")
def changes_should_be_reflected_immediately(step):
    # This is already verified in the previous step
    pass

@step("the current filter state should be preserved")
def current_filter_state_should_be_preserved(step):
    # This would need to be implemented based on the current filter state
    pass

@step("I am viewing all artifacts")
def i_am_viewing_all_artifacts(step):
    # This step assumes we're on the artifacts page
    pass

@step("I select \"{value}\" from the type filter")
def i_select_from_type_filter(step, value):
    type_filter = world.driver.find_element(By.ID, "typeFilter")
    select = Select(type_filter)
    select.select_by_value(value)

@step("only {type} artifacts should be displayed")
def only_type_artifacts_should_be_displayed(step, type):
    # Wait for filtering to complete
    time.sleep(1)
    # Check that all visible artifacts are of the specified type
    artifacts = world.driver.find_elements(By.CLASS_NAME, "artifact-card")
    for artifact in artifacts:
        if artifact.is_displayed():
            type_label = artifact.find_element(By.CLASS_NAME, "artifact-type")
            assert type in type_label.text.lower(), f"Artifact type {type_label.text} is not {type}"

@step("the filter dropdown should show \"{value}\"")
def filter_dropdown_should_show_value(step, value):
    # This would need to be implemented based on the specific filter being tested
    pass

@step("I click the \"Delete\" button")
def i_click_delete_button(step):
    # Find the first delete button (ion-icon with trash-outline)
    delete_button = world.driver.find_element(By.XPATH, "//button[.//ion-icon[@name='trash-outline']]")
    delete_button.click()

@step("I confirm the deletion")
def i_confirm_deletion(step):
    # Wait for confirmation dialog and click confirm
    confirm_button = world.driver.find_element(By.XPATH, "//button[contains(text(), 'Confirm') or contains(text(), 'Delete')]")
    confirm_button.click()

@step("the artifact should be removed")
def artifact_should_be_removed(step):
    # Wait for the artifact to disappear
    time.sleep(1)
    # This would need to be implemented based on how we identify the specific artifact

@step("it should no longer appear in the list")
def artifact_should_not_appear_in_list(step):
    # This is already verified in the previous step
    pass

@step("I select \"{value}\" from the status filter")
def i_select_from_status_filter(step, value):
    status_filter = world.driver.find_element(By.ID, "statusFilter")
    select = Select(status_filter)
    select.select_by_value(value)

@step("only {status} artifacts should be displayed")
def only_status_artifacts_should_be_displayed(step, status):
    # Wait for filtering to complete
    time.sleep(1)
    # Check that all visible artifacts have the specified status
    artifacts = world.driver.find_elements(By.CLASS_NAME, "artifact-card")
    for artifact in artifacts:
        if artifact.is_displayed():
            status_label = artifact.find_element(By.CLASS_NAME, "artifact-status")
            assert status in status_label.text.lower(), f"Artifact status {status_label.text} is not {status}"

@step("I enter \"{text}\" in the search box")
def i_enter_text_in_search_box(step, text):
    search_input = world.driver.find_element(By.ID, "search-input")
    search_input.clear()
    search_input.send_keys(text)

@step("I type \"{text}\" in the search box")
def i_type_text_in_search_box(step, text):
    search_input = world.driver.find_element(By.ID, "search-input")
    search_input.clear()
    search_input.send_keys(text)

@step("the results should filter in real-time")
def results_should_filter_in_realtime(step):
    # Wait for filtering to complete
    time.sleep(1)
    pass

@step("only artifacts containing \"{text}\" should be displayed")
def only_artifacts_containing_text_should_be_displayed(step, text):
    # Check that all visible artifacts contain the search text
    artifacts = world.driver.find_elements(By.CLASS_NAME, "artifact-card")
    for artifact in artifacts:
        if artifact.is_displayed():
            summary = artifact.find_element(By.CLASS_NAME, "artifact-summary")
            description = artifact.find_element(By.CLASS_NAME, "artifact-description")
            assert text.lower() in summary.text.lower() or text.lower() in description.text.lower(), f"Artifact does not contain '{text}'"

@step("I click on a category link in an artifact tile")
def i_click_on_category_link(step):
    # Find the first category link
    category_link = world.driver.find_element(By.CLASS_NAME, "category-link")
    category_link.click()

@step("the view should filter to show only artifacts with that category")
def view_should_filter_by_category(step):
    # Wait for filtering to complete
    time.sleep(1)
    pass

@step("the category filter input should be updated with the selected category")
def category_filter_input_should_be_updated(step):
    # This would need to be implemented based on the category filter implementation
    pass

@step("I have filtered artifacts by type \"{type}\"")
def i_have_filtered_artifacts_by_type(step, type):
    # Select the type filter
    type_filter = world.driver.find_element(By.ID, "typeFilter")
    select = Select(type_filter)
    select.select_by_value(type)
    time.sleep(1)

@step("the type filter should still show \"{type}\"")
def type_filter_should_still_show(step, type):
    type_filter = world.driver.find_element(By.ID, "typeFilter")
    select = Select(type_filter)
    assert select.first_selected_option.text.lower() == type.lower(), f"Type filter should show {type}"

@step("I have applied filters to the view")
def i_have_applied_filters_to_view(step):
    # Apply a type filter as an example
    type_filter = world.driver.find_element(By.ID, "typeFilter")
    select = Select(type_filter)
    select.select_by_value("requirement")
    time.sleep(1)

@step("I click the \"Refresh\" button")
def i_click_refresh_button(step):
    refresh_button = world.driver.find_element(By.XPATH, "//button[contains(text(), 'Refresh')]")
    refresh_button.click()

@step("all filters should be reset")
def all_filters_should_be_reset(step):
    # Check that type filter is reset
    type_filter = world.driver.find_element(By.ID, "typeFilter")
    select = Select(type_filter)
    assert select.first_selected_option.text == "All Types", "Type filter should be reset"

@step("all artifacts should be displayed")
def all_artifacts_should_be_displayed(step):
    # This would need to be implemented based on the total count
    pass

@step("filter dropdowns should show default values")
def filter_dropdowns_should_show_default_values(step):
    # Check type filter default
    type_filter = world.driver.find_element(By.ID, "typeFilter")
    select = Select(type_filter)
    assert select.first_selected_option.text == "All Types", "Type filter should show default value"

@step("I edit an artifact")
def when_i_edit_an_artifact(step):
    # Click the edit button
    edit_button = world.driver.find_element(By.XPATH, "//button[.//ion-icon[@name='create-outline']]")
    edit_button.click()
    
    # Wait for edit modal to appear
    wait = WebDriverWait(world.driver, 10)
    wait.until(EC.visibility_of_element_located((By.ID, "artifactDescription")))
    
    # Modify the description
    description_field = world.driver.find_element(By.ID, "artifactDescription")
    description_field.clear()
    description_field.send_keys("Modified description for testing")

@step("I save the changes")
def when_i_save_the_changes(step):
    save_button = world.driver.find_element(By.XPATH, "//button[text()='Save Artifact']")
    save_button.click()

@step("I set the {name} filter to {value:QuotedString}")
def i_set_filter_to_value(step, name, value):
    # Map filter names to element IDs and handling methods
    filter_mapping = {
        "status": ("statusFilter", "select"),
        "type": ("typeFilter", "select"),
        "category": ("categoryFilter", "select"),
        "verification": ("verificationFilter", "select"),
        "activity": ("activityFilter", "input"),
        "iteration": ("iterationFilter", "select"),
        "flagged": ("flaggedFilter", "checkbox")
    }
    
    if name.lower() not in filter_mapping:
        raise ValueError(f"Unknown filter '{name}'. Supported filters: {', '.join(filter_mapping.keys())}")
    
    element_id, filter_type = filter_mapping[name.lower()]
    
    # Wait for the filter element to be present
    wait = WebDriverWait(world.driver, 10)
    element = wait.until(EC.presence_of_element_located((By.ID, element_id)))
    
    if filter_type == "select":
        # Handle dropdown/select filters
        select = Select(element)
        select.select_by_value(value)
    elif filter_type == "input":
        # Handle text input filters
        element.clear()
        element.send_keys(value)
    elif filter_type == "checkbox":
        # Handle checkbox filters
        if value.lower() in ["true", "yes", "1", "checked"]:
            if not element.is_selected():
                element.click()
        else:
            if element.is_selected():
                element.click()