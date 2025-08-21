from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from controls.base import ControlBase
from controls.button import Button


class Toolbar:
    """Control class for toolbar interactions."""
    
    def __init__(self, driver=None):
        """Initialize the Toolbar control.
        
        Args:
            driver: WebDriver instance (optional, will use world.driver if not provided)
        """
        if driver is None:
            from radish import world
            self.driver = world.driver
        else:
            self.driver = driver
    
    @property
    def filter(self):
        """Access to filter controls in the toolbar."""
        return FilterControls(self.driver)
    
    def wait_for_toolbar(self, timeout=10):
        """Wait for the toolbar to be visible and loaded."""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located((By.ID, "toolbar")))


class FilterControls:
    """Control class for filter-specific interactions in the toolbar."""
    
    def __init__(self, driver):
        """Initialize the FilterControls.
        
        Args:
            driver: WebDriver instance
        """
        self.driver = driver
    
    @property
    def flag(self):
        """Access to the flag filter button."""
        return Button("flagFilter", self.driver)
    
    @property
    def status(self):
        """Access to the status filter dropdown."""
        return StatusFilter(self.driver)
    
    @property
    def type(self):
        """Access to the type filter dropdown."""
        return TypeFilter(self.driver)
    
    @property
    def category(self):
        """Access to the category filter dropdown."""
        return CategoryFilter(self.driver)
    
    @property
    def verification(self):
        """Access to the verification filter dropdown."""
        return VerificationFilter(self.driver)
    
    @property
    def activity(self):
        """Access to the activity filter input."""
        return ActivityFilter(self.driver)
    
    @property
    def iteration(self):
        """Access to the iteration filter dropdown."""
        return IterationFilter(self.driver)


class StatusFilter(ControlBase):
    """Control class for the status filter dropdown."""
    
    def __init__(self, driver):
        """Initialize the StatusFilter control.
        
        Args:
            driver: WebDriver instance
        """
        super().__init__("statusFilter")
        self.driver = driver
    
    def select(self, value):
        """Select a status value from the dropdown."""
        from selenium.webdriver.support.ui import Select
        element = self.find_element(self.driver)
        select = Select(element)
        select.select_by_value(value)
        return self


class TypeFilter(ControlBase):
    """Control class for the type filter dropdown."""
    
    def __init__(self, driver):
        """Initialize the TypeFilter control.
        
        Args:
            driver: WebDriver instance
        """
        super().__init__("typeFilter")
        self.driver = driver
    
    def select(self, value):
        """Select a type value from the dropdown."""
        from selenium.webdriver.support.ui import Select
        element = self.find_element(self.driver)
        select = Select(element)
        select.select_by_value(value)
        return self


class CategoryFilter(ControlBase):
    """Control class for the category filter dropdown."""
    
    def __init__(self, driver):
        """Initialize the CategoryFilter control.
        
        Args:
            driver: WebDriver instance
        """
        super().__init__("categoryFilter")
        self.driver = driver
    
    def select(self, value):
        """Select a category value from the dropdown."""
        from selenium.webdriver.support.ui import Select
        element = self.find_element(self.driver)
        select = Select(element)
        select.select_by_value(value)
        return self


class VerificationFilter(ControlBase):
    """Control class for the verification filter dropdown."""
    
    def __init__(self, driver):
        """Initialize the VerificationFilter control.
        
        Args:
            driver: WebDriver instance
        """
        super().__init__("verificationFilter")
        self.driver = driver
    
    def select(self, value):
        """Select a verification value from the dropdown."""
        from selenium.webdriver.support.ui import Select
        element = self.find_element(self.driver)
        select = Select(element)
        select.select_by_value(value)
        return self


class ActivityFilter(ControlBase):
    """Control class for the activity filter input."""
    
    def __init__(self, driver):
        """Initialize the ActivityFilter control.
        
        Args:
            driver: WebDriver instance
        """
        super().__init__("activityFilter")
        self.driver = driver
    
    def set_value(self, value):
        """Set the activity filter value."""
        element = self.find_element(self.driver)
        element.clear()
        element.send_keys(value)
        return self


class IterationFilter(ControlBase):
    """Control class for the iteration filter dropdown."""
    
    def __init__(self, driver):
        """Initialize the IterationFilter control.
        
        Args:
            driver: WebDriver instance
        """
        super().__init__("iterationFilter")
        self.driver = driver
    
    def select(self, value):
        """Select an iteration value from the dropdown."""
        from selenium.webdriver.support.ui import Select
        element = self.find_element(self.driver)
        select = Select(element)
        select.select_by_value(value)
        return self
