from selenium.webdriver.common.by import By
from radish import step, world

from bdd.controls.artifact_control import Artifacts
from bdd.controls.editor import Editor
from logging_config import logger as log


@step("I create a new requirement")
def i_create_a_new_requirement(step):
    editor = Editor(world.driver)
    log.trace("Editor control created, opening modal...")
    editor.open()


@step("I create a new requirement with name {name:QuotedString}")
def i_create_a_new_requirement_with_name(step, name):
    editor = Editor(world.driver)
    editor.open()
    editor.set("summary", name)


@step("I set the {field} to {value:QuotedString}")
def i_set_field_to(step, field, value):
    editor = Editor(world.driver)
    editor.set(field, value)


@step("I see the new artifact in the list")
def i_see_new_artifact_in_list(step):
    Artifacts().find_one(summary="Test requirement for BDD testing")


@step("I cancel the artifact creation")
def i_cancel_artifact_creation(step):
    editor = Editor(world.driver)
    editor.cancel()


@step("I search for artifacts with {search_text:QuotedString}")
def i_search_for_artifacts_with(step, search_text):
    # Find the search input field
    search_input = world.driver.find_element(By.ID, "search-input")
    log.trace("Found search input field")

    # Clear and enter search text
    search_input.clear()
    search_input.send_keys(search_text)
    log.trace(f"Entered search text: '{search_text}'")

    # Wait for search to complete (if there's a search button, click it)
    try:
        search_button = world.driver.find_element(By.ID, "searchButton")
        search_button.click()
    except Exception:
        # No search button, search might be automatic
        pass


@step("I see {count:d} search results")
def i_see_search_results(step, count):
    results = Artifacts().find()
    actual_count = len(results)
    assert actual_count == count, f"Expected {count}, but got {actual_count}"
