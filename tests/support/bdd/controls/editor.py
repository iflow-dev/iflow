"""
Editor control class for BDD test automation.
This module provides controls for managing artifact creation and editing in the modal.
"""

import sys
import os
import time
import traceback
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from controls.base import ControlBase
from controls.input_field import InputField
from controls.button import Button
from controls.page import Page
from controls.toolbar import Toolbar
from controls.flag import Flag
from controls.dropdown import CustomDropdown

from bdd.logging import logger

class Editor(ControlBase):

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

        # Flag control
        self.flag = Flag(driver)

        # Button controls
        self.submit_button = Button("submit", None, None)  # Will find any submit button regardless of text
        self.cancel_button = Button("button", "Cancel", None)  # Button with text "Cancel"

    def open(self):
        logger.trace("Waiting for toolbar to be fully loaded...")

        # Wait for the toolbar to be fully loaded (not just the loading message)
        page = Page()
        page.wait()

        # Use Toolbar pattern to access create button
        toolbar = Toolbar(self.driver)

        # Use the new Toolbar().buttons.create pattern
        logger.trace("Clicking create button via Toolbar().buttons.create...")
        toolbar.buttons.create.click()

        # Wait for modal to be visible using locate()
        self.locate()

        return self

    def close(self):
        self.cancel_button.click()
        return self

    def set(self, field, value):
        """Generic method to set any artifact field to a specified value."""
        logger.trace(f"Setting field '{field}' to value '{value}'")

        # Map field names to element IDs and handling methods
        field_mapping = {
            "type": ("artifactType", "select"),
            "summary": ("artifactSummary", "input"),
            "description": ("artifactDescription", "textarea"),
            "category": ("artifactCategory", "input"),
            "status": ("artifactStatus", "select"),
            "verification": ("artifactVerification", "input"),
            "activity": ("artifactActivity", "input"),
            "iteration": ("artifactIteration", "input"),
            "flagged": ("artifactFlagged", "checkbox")
        }

        if field.lower() not in field_mapping:
            raise ValueError(f"Unknown field '{field}'. Supported fields: {', '.join(field_mapping.keys())}")

        element_id, field_type = field_mapping[field.lower()]

        # Use CustomDropdown for select fields
        if field_type == "select":
            dropdown = CustomDropdown(self.driver.find_element(By.ID, element_id))
            dropdown.set_value(value)
            logger.trace(f"Set dropdown field '{field}' to '{value}' using {dropdown.__class__.__name__}")
        elif field_type in ["input", "textarea"]:
            # For input and textarea fields, find the element and set value
            wait = WebDriverWait(self.driver, 10)
            element = wait.until(EC.element_to_be_clickable((By.ID, element_id)))
            element.clear()
            element.send_keys(value)
            logger.trace(f"Set {field_type} field '{field}' to '{value}'")
        elif field_type == "checkbox":
            # Handle checkbox fields
            wait = WebDriverWait(self.driver, 10)
            element = wait.until(EC.element_to_be_clickable((By.ID, element_id)))
            should_check = value.lower() in ["true", "yes", "1", "checked"]
            if should_check != element.is_selected():
                element.click()
            logger.trace(f"{'Checked' if should_check else 'Unchecked'} checkbox field '{field}'")

    def create(self):
        """Create the artifact and close the modal."""
        self.submit_button.click()
        return self.clear()

    def save(self):
        self.submit_button.click()
        return self.clear()

    def cancel(self):
        self.cancel_button.click()
        return self.clear()

    def clear(self, timeout=2):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.invisibility_of_element_located((By.ID, "artifactModal")))
        return self

    @property
    def status(self):
        """Get the current status field value from the editor."""
        try:
            wait = WebDriverWait(self.driver, 10)
            # Locate the element for the status field
            element = wait.until(EC.visibility_of_element_located((By.ID, "artifactStatus")))
            
            # Try to get the value from the native select element first
            try:
                select = Select(element)
                return select.first_selected_option.get_attribute("value")
            except Exception:
                # If Select fails, try to get the value directly from the element
                return element.get_attribute("value")
        except Exception as e:
            logger.error(f"Failed to get status field value: {e}")
            return None
