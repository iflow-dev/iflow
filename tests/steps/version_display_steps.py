from radish import step, world
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@step("I see version information in the header")
def i_see_version_in_header(step):
    """Verify that version information is displayed in the header."""
    from radish import world
    
    try:
        # Wait for the header version element to be present
        header_version = WebDriverWait(world.driver, 10).until(
            EC.presence_of_element_located((By.ID, "header-version"))
        )
        
        # Check that the version text is not empty
        version_text = header_version.text.strip()
        assert version_text, "Version information should be displayed in header"
        assert version_text.startswith('v'), f"Version should start with 'v', got: {version_text}"
        
        print(f"✅ Version information found in header: {version_text}")
        
    except Exception as e:
        raise AssertionError(f"Version information not found in header: {e}")


@step("I do not see version information in the statistics line")
def i_do_not_see_version_in_stats(step):
    """Verify that version information is NOT displayed in the statistics line."""
    from radish import world
    
    try:
        # Find the statistics bar
        stats_bar = world.driver.find_element(By.ID, "stats-bar")
        
        # Check that no version information is present in the stats bar
        stats_text = stats_bar.text.lower()
        
        # Version-related terms that should not be present
        version_terms = ['version', 'v1', 'v2', 'v3', 'v4', 'v5']
        
        for term in version_terms:
            assert term not in stats_text, f"Version information '{term}' should not be in statistics line"
        
        print("✅ No version information found in statistics line")
        
    except Exception as e:
        raise AssertionError(f"Error checking statistics line for version information: {e}")


@step("I see the statistics line")
def i_see_statistics_line(step):
    """Verify that the statistics line is visible."""
    from radish import world
    
    try:
        # Wait for the statistics bar to be present
        stats_bar = WebDriverWait(world.driver, 10).until(
            EC.presence_of_element_located((By.ID, "stats-bar"))
        )
        
        # Check that it's visible
        assert stats_bar.is_displayed(), "Statistics line should be visible"
        
        print("✅ Statistics line is visible")
        
    except Exception as e:
        raise AssertionError(f"Statistics line not found or not visible: {e}")


@step("the statistics line does not contain version information")
def stats_line_no_version(step):
    """Verify that the statistics line does not contain version information."""
    from radish import world
    
    try:
        # Find the statistics bar
        stats_bar = world.driver.find_element(By.ID, "stats-bar")
        
        # Get all stat items
        stat_items = stats_bar.find_elements(By.CLASS_NAME, "stat-item")
        
        # Check that none of the stat items contain version information
        for item in stat_items:
            item_text = item.text.lower()
            
            # Check for version-related content
            if 'version' in item_text or any(item_text.startswith(f'v{i}') for i in range(1, 10)):
                raise AssertionError(f"Statistics line contains version information: {item_text}")
        
        print("✅ Statistics line does not contain version information")
        
    except Exception as e:
        raise AssertionError(f"Error verifying statistics line content: {e}")
