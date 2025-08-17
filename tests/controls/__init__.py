"""
Control classes for BDD test automation.
This module provides page object pattern classes for interacting with web elements.
"""

from selenium.webdriver.common.by import By


class ControlBase:
    def __init__(self, xpath):
        self.xpath = xpath

    def locate(self, driver, timeout=5):
        """Locate the element within timeout, assert if not found."""
        import logging
        logging.basicConfig(level=logging.DEBUG)
        logger = logging.getLogger(__name__)
        
        logger.debug(f"Looking for element with XPath: {self.xpath}")
        
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        wait = WebDriverWait(driver, timeout)
        element = wait.until(EC.presence_of_element_located((By.XPATH, self.xpath)))
        
        logger.debug(f"Found element: {element.text[:100]}...")
        return element

    def get_text(self, driver, timeout=5):
        return self.locate(driver, timeout).text
        
    def exists(self, driver, timeout=5):
        """Wait for element to appear and return true/false."""
        try:
            self.locate(driver, timeout)
            return True
        except:
            return False
    
    def click(self, driver, timeout=5):
        """Click the element after locating it."""
        element = self.locate(driver, timeout)
        element.click()
        return element


class Editor(ControlBase):
    """Control for managing artifact creation and editing in the modal."""
    
    def __init__(self, driver):
        """Initialize the artifact editor control."""
        # The editor operates within the artifact modal
        super().__init__("//div[@id='artifactModal']")
        
        # Store the driver for internal use
        self.driver = driver
        
        # Initialize field controls
        self.summary_field = InputField("summary")
        self.description_field = InputField("description")
        self.category_field = InputField("category")
        self.status_field = InputField("status")
        self.type_field = InputField("type")
        
        # Button controls
        self.create_button = Button("Create", context="modal")
        self.cancel_button = Button("Cancel", context="modal")
    
    def open(self):
        """Open the artifact creation modal."""
        from controls import Button
        create_button = Button("Create", context="toolbar")
        create_button.click(self.driver)
        
        # Wait for modal to be visible using locate()
        self.locate(self.driver)
        return self
    
    def close(self):
        """Close the artifact creation modal."""
        from controls import Button
        close_button = Button("×", context="modal")
        try:
            close_button.click(self.driver)
        except:
            # If close button not found, try cancel button
            self.cancel_button.click(self.driver)
    
    def set_summary(self, summary):
        """Set the artifact summary."""
        return self.summary_field.set_value(self.driver, summary)
    
    def set_description(self, description):
        """Set the artifact description."""
        return self.description_field.set_value(self.driver, description)
    
    def set_category(self, category):
        """Set the artifact category."""
        return self.category_field.set_value(self.driver, category)
    
    def set_status(self, status):
        """Set the artifact status."""
        return self.status_field.set_value(self.driver, status)
    
    def set_type(self, artifact_type):
        """Set the artifact type."""
        return self.type_field.set_value(self.driver, artifact_type)
    
    def get_summary(self):
        """Get the current artifact summary."""
        return self.summary_field.get_value(self.driver)
    
    def get_description(self):
        """Get the current artifact description."""
        return self.description_field.get_value(self.driver)
    
    def get_category(self):
        """Get the current artifact category."""
        return self.category_field.get_value(self.driver)
    
    def get_status(self):
        """Get the current artifact status."""
        return self.status_field.get_value(self.driver)
    
    def get_type(self):
        """Get the current artifact type."""
        return self.type_field.get_value(self.driver)
    
    def create(self):
        """Create the artifact and close the modal."""
        self.create_button.click(self.driver)
        
        # Wait for modal to close (modal should disappear)
        try:
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.common.by import By
            
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.invisibility_of_element_located((By.ID, "artifactModal")))
        except:
            # If modal doesn't close automatically, force close it
            self.close()
        
        return True
    
    def cancel(self):
        """Cancel artifact creation and close the modal."""
        self.cancel_button.click(self.driver)
        
        # Wait for modal to close
        try:
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.common.by import By
            
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.invisibility_of_element_located((By.ID, "artifactModal")))
        except:
            # If modal doesn't close automatically, force close it
            self.close()
        
        return True
    
    def abort(self):
        """Abort artifact creation (same as cancel)."""
        return self.cancel()
    
    def is_open(self):
        """Check if the editor modal is currently open."""
        try:
            from selenium.webdriver.common.by import By
            modal = self.driver.find_element(By.ID, "artifactModal")
            return modal.is_displayed()
        except:
            return False
    
    def is_closed(self):
        """Check if the editor modal is currently closed."""
        return not self.is_open()
    
    def wait_for_visible(self, timeout=5):
        """Wait for the editor modal to become visible."""
        # Use the existing locate method which already handles waiting
        self.locate(self.driver, timeout)
        return True


class Title(ControlBase):
    def __init__(self, text):
        super().__init__(f"//h1[contains(text(), '{text}')]")


class Navigation(ControlBase):
    def __init__(self, driver):
        super().__init__("//nav")


class Tile(ControlBase):
    def __init__(self, tile_id):
        super().__init__(f"//div[@class='artifact-card' and contains(., '{tile_id}')]")


class Button(ControlBase):
    """Control for locating and interacting with buttons."""
    
    def __init__(self, text, context=None):
        """
        Initialize button control with text content.
        
        Args:
            text: Button text content (e.g., "Create", "Save", "Cancel")
            context: Optional context to narrow down the search (e.g., "modal", "toolbar")
        """
        if context == "modal":
            # For buttons inside the modal, look within the modal context
            xpath = f"//div[@id='artifactModal']//button[contains(text(), '{text}')]"
        elif context == "toolbar":
            # For buttons in the toolbar, look in the toolbar context
            xpath = f"//div[@class='toolbar']//button[contains(text(), '{text}')]"
        else:
            # Default: look for any button with the text
            xpath = f"//button[contains(text(), '{text}')]"
        super().__init__(xpath)


class Modal(ControlBase):
    """Control for locating and interacting with modal dialogs."""
    
    def __init__(self, identifier=None):
        """
        Initialize modal control.
        
        Args:
            identifier: Optional identifier for the modal (text, class, or id)
        """
        if identifier == "create":
            # For create modal, look for modal with "Create New Artifact" title
            xpath = "//div[@id='artifactModal' and @class='modal']"
        elif identifier:
            xpath = f"//div[contains(@class, 'modal') and contains(., '{identifier}')]"
        else:
            xpath = "//div[contains(@class, 'modal')]"
        super().__init__(xpath)
    
    def is_visible(self, driver, timeout=5):
        """Check if the modal is currently visible."""
        try:
            element = self.locate(driver, timeout)
            return element.is_displayed()
        except:
            return False
    
    def wait_for_visible(self, driver, timeout=5):
        """Wait for modal to become visible."""
        element = self.locate(driver, timeout)
        if not element.is_displayed():
            raise AssertionError(f"Modal found but not visible after {timeout} seconds")
        return element


class InputField(ControlBase):
    """Control for locating and interacting with input fields."""
    
    def __init__(self, field_type):
        """
        Initialize input field control.
        
        Args:
            field_type: Type of input field (e.g., "summary", "description", "status")
        """
        if field_type == "summary":
            xpath = "//input[@id='artifactSummary']"
        elif field_type == "description":
            xpath = "//textarea[@id='artifactDescription']"
        elif field_type == "category":
            xpath = "//input[@id='artifactCategory']"
        elif field_type == "status":
            xpath = "//select[@id='artifactStatus']"
        elif field_type == "type":
            xpath = "//select[@id='artifactType']"
        else:
            xpath = f"//input[@name='{field_type}' or @id='{field_type}' or @placeholder='{field_type}']"
        super().__init__(xpath)
    
    def set_value(self, driver, value, timeout=5):
        """Set the value of the input field."""
        element = self.locate(driver, timeout)
        
        # Handle different element types
        tag_name = element.tag_name.lower()
        if tag_name == 'select':
            # For select elements, use select_by_value
            from selenium.webdriver.support.ui import Select
            select = Select(element)
            select.select_by_value(value)
        else:
            # For input/textarea elements, clear and send keys
            element.clear()
            element.send_keys(value)
        
        return element
    
    def get_value(self, driver, timeout=5):
        """Get the current value of the input field."""
        element = self.locate(driver, timeout)
        return element.get_attribute("value")
