import logging

from radish import given, when, then, step

from selenium.webdriver.common.by import By

from bdd.controls import Title

# Set up logging
log = logging.getLogger(__name__)

@then("I see version information in the header")
def i_see_version_information_in_header(step):
    """Verify that version information is displayed in the header."""
    from radish import world
    from bdd.controls import Title
    
    # Look for version information in the header
    try:
        version_element = world.driver.find_element(By.ID, "header-version")
        version_text = version_element.text
        log.debug(f"✅ Version information found in header: {version_text}")
    except Exception as e:
        raise AssertionError(f"Version information not found in header: {e}")

@then("I do not see version information in the statistics line")
def i_do_not_see_version_in_statistics_line(step):
    """Verify that version information is not displayed in the statistics line."""
    from radish import world
    
    # Look for version information in the statistics line
    try:
        stats_element = world.driver.find_element(By.ID, "stats-bar")
        stats_text = stats_element.text
        
        # Check if version information is present in the statistics
        if "v" in stats_text and any(char.isdigit() for char in stats_text):
            # This is a simple check - we could make it more sophisticated
            raise AssertionError("Version information found in statistics line")
        
        log.debug("✅ No version information found in statistics line")
    except Exception as e:
        if "Version information found" in str(e):
            raise e
        log.debug(f"Statistics line not found or error checking: {e}")

@then("I see the statistics line")
def i_see_statistics_line(step):
    """Verify that the statistics line is displayed."""
    from radish import world
    
    try:
        stats_element = world.driver.find_element(By.ID, "stats-bar")
        if stats_element.is_displayed():
            log.debug("✅ Statistics line is visible")
        else:
            raise AssertionError("Statistics line is not visible")
    except Exception as e:
        raise AssertionError(f"Statistics line not found: {e}")

@then("the statistics line does not contain version information")
def statistics_line_does_not_contain_version(step):
    """Verify that the statistics line does not contain version information."""
    from radish import world
    
    try:
        stats_element = world.driver.find_element(By.ID, "stats-bar")
        stats_text = stats_element.text
        
        # Look for version-like patterns in the statistics
        import re
        version_pattern = r'v\d+\.\d+\.\d+'
        if re.search(version_pattern, stats_text):
            raise AssertionError("Version information found in statistics line")
        
        # Also check for simple version indicators
        if "version" in stats_text.lower():
            raise AssertionError("Version information found in statistics line")
        
        log.debug("✅ Statistics line does not contain version information")
    except Exception as e:
        if "Version information found" in str(e):
            raise e
        log.debug(f"Error checking statistics line: {e}")
