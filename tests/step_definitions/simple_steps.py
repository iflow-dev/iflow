"""
Simple step definitions for basic functionality testing.
"""

from radish import given, then
from selenium.webdriver.common.by import By

class ControlBase:
    def __init__(self, xpath):
        self.xpath = xpath

    def locate(self, driver, timeout=5):
        """Locate the element within timeout, assert if not found."""
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        wait = WebDriverWait(driver, timeout)
        return wait.until(EC.presence_of_element_located((By.XPATH, self.xpath)))

    def get_text(self, driver, timeout=5):
        return self.locate(driver, timeout).text
        
    def exists(self, driver, timeout=5):
        """Wait for element to appear and return true/false."""
        try:
            self.locate(driver, timeout)
            return True
        except:
            return False

class Title(ControlBase):
    def __init__(self, text):
        super().__init__(f"//h1[contains(text(), '{text}')]")

class Navigation(ControlBase):
    def __init__(self):
        super().__init__("//nav")

@given("I go to home")
def i_go_to_home(step):
    """Navigate to the home page (base URL)."""
    from radish import world
    base_url = getattr(step.context, 'base_url', 'http://localhost:8081')
    world.driver.get(base_url)
    
    # check the driver url after navigation (allow for redirects)
    assert base_url in world.driver.current_url
    
    # Wait for the page to load
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    wait = WebDriverWait(world.driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "artifacts-container")))

@given("I am on the search page")
def i_am_on_search_page(step):
    """Check that we are on the search page (expects previous step to have navigated)."""
    from radish import world
    title = Title("iflow")
    title.locate(world.driver)

@then("the page title should be displayed")
def page_title_should_be_displayed(step):
    """Verify the page title is displayed."""
    from radish import world
    title = Title("iflow")
    title.locate(world.driver)
