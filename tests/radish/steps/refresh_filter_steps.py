"""
Step definitions for refresh filter functionality.
"""

from radish import given, when, then, step
from selenium.webdriver.common.by import By

from bdd.logging_config import logger as log


@given("I filter for type {filter_value}")
def filter_for_type(step, filter_value):
    """Apply a type filter with the specified value."""
    from radish import world
    from time import sleep

    # Strip quotes from the filter value
    filter_value = filter_value.strip('"')

    log.trace(f"Debug: Setting up type filter for '{filter_value}'")

    # Use the TypeFilter control to select the option
    from bdd.controls.toolbar import TypeFilter
    type_filter = TypeFilter(world.driver)
    type_filter.select(filter_value)

    # Wait for the filtering to be applied
    sleep(2)

    # Verify that filtering worked by checking the number of displayed artifacts
    artifacts = world.driver.find_elements(By.CSS_SELECTOR, ".artifact-card")
    log.trace(f"Debug: Found {len(artifacts)} artifacts after applying type filter '{filter_value}'")


@given("I filter for status {filter_value}")
def filter_for_status(step, filter_value):
    """Apply a status filter with the specified value."""
    from radish import world
    from time import sleep

    # Strip quotes from the filter value
    filter_value = filter_value.strip('"')

    log.trace(f"Debug: Setting up status filter for '{filter_value}'")

    # Use the StatusFilter control to select the option
    from bdd.controls.toolbar import StatusFilter
    status_filter = StatusFilter(world.driver)
    status_filter.select(filter_value)

    # Wait for the filtering to be applied
    sleep(2)

    # Verify that filtering worked by checking the number of displayed artifacts
    artifacts = world.driver.find_elements(By.CSS_SELECTOR, ".artifact-card")
    log.trace(f"Debug: Found {len(artifacts)} artifacts after applying status filter '{filter_value}'")


@when("I refresh the view")
def refresh_the_view(step):
    """Refresh the view by clicking the refresh button."""
    from radish import world
    from time import sleep

    # Close any open dropdowns by clicking outside of them
    try:
        body = world.driver.find_element(By.TAG_NAME, "body")
        body.click()
        sleep(0.5)
    except Exception:
        pass

    # Find and click the refresh button
    refresh_button = world.driver.find_element(By.CSS_SELECTOR, "button[title='Refresh artifacts']")
    refresh_button.click()

    # Wait for refresh to complete
    sleep(2)


@then("I see the type filter is set to {expected_value}")
def see_type_filter_set_to(step, expected_value):
    """Check that the type filter shows the expected value."""
    from radish import world
    from selenium.webdriver.support.ui import Select
    from selenium.webdriver.common.by import By

    # Strip quotes from expected value
    expected_value = expected_value.strip('"')

    # Find the type filter element and get its selected value
    type_filter = world.driver.find_element(By.ID, "typeFilter")
    select = Select(type_filter)
    selected_option = select.first_selected_option

    if selected_option:
        actual_value = selected_option.text.strip()
        log.trace(f"Debug: Type filter shows '{actual_value}', expected '{expected_value}'")

        # Check if the expected value is in the actual text (case insensitive)
        assert expected_value.lower() in actual_value.lower(), (
            f"Type filter should show '{expected_value}', but shows '{actual_value}'")
    else:
        assert False, "No option selected in type filter"


@step("I see the status filter is set to {expected_value:QuotedString}")
def see_status_filter_set_to(step, expected_value):
    """Check that the status filter shows the expected value."""
    from radish import world
    from selenium.webdriver.support.ui import Select
    from selenium.webdriver.common.by import By

    # Strip quotes from expected value
    expected_value = expected_value.strip('"')

    # Find the status filter element and get its selected value
    status_filter = world.driver.find_element(By.ID, "statusFilter")
    select = Select(status_filter)
    selected_option = select.first_selected_option

    if selected_option:
        actual_value = selected_option.text.strip()
        log.trace(f"Debug: Status filter shows '{actual_value}', expected '{expected_value}'")

        # Check if the expected value is in the actual text (case insensitive)
        assert expected_value.lower() in actual_value.lower(), (
            f"Status filter should show '{expected_value}', but shows '{actual_value}'")
    else:
        assert False, "No option selected in status filter"


@then("I only see requirement items")
def only_see_requirement_items(step):
    """Check that only requirement items are displayed."""
    from radish import world

    # Check that artifacts are filtered to show only requirements
    artifacts = world.driver.find_elements(By.CSS_SELECTOR, ".artifact-card")

    # Should see some artifacts
    assert len(artifacts) > 0, "Should see some requirement items"

    # Check that all artifacts are of type "requirement"
    for artifact in artifacts:
        artifact_text = artifact.text.lower()
        assert "requirement" in artifact_text, (
            f"Artifact should be of type 'requirement': {artifact_text[:100]}")


@then("I only see requirement items with open status")
def only_see_requirement_items_with_open_status(step):
    """Check that only requirement items with open status are displayed."""
    from radish import world

    # Check that artifacts are filtered to show only requirements with open status
    artifacts = world.driver.find_elements(By.CSS_SELECTOR, ".artifact-card")

    # Should see some artifacts
    assert len(artifacts) > 0, "Should see some requirement items with open status"

    # Check that all artifacts are of type "requirement" and have "open" status
    for artifact in artifacts:
        artifact_text = artifact.text.lower()

        # Should contain "requirement" (type filter)
        assert "requirement" in artifact_text, (
            f"Artifact should be of type 'requirement': {artifact_text[:100]}")

        # Should contain "open" (status filter)
        assert "open" in artifact_text, (
            f"Artifact should have 'open' status: {artifact_text[:100]}")
