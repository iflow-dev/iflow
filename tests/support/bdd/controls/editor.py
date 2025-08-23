"""
Editor control class for BDD test automation.
This module provides controls for managing artifact creation and editing in the modal.
"""

import sys
import os
import logging
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

# Set up logging
log = logging.getLogger(__name__)


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
        log.trace("Waiting for toolbar to be fully loaded...")

        # Wait for the toolbar to be fully loaded (not just the loading message)
        page = Page()
        page.wait()

        # Use Toolbar pattern to access create button
        toolbar = Toolbar(self.driver)

        # Use the new Toolbar().buttons.create pattern
        log.trace("Clicking create button via Toolbar().buttons.create...")
        toolbar.buttons.create.click()

        # Wait for modal to be visible using locate()
        self.locate()

        return self

    def close(self):
        self.cancel_button.click()
        return self

    def set(self, field, value):
        """Generic method to set any artifact field to a specified value."""
        log = logging.getLogger(__name__)
        log.trace(f"Setting field '{field}' to value '{value}'")

        try:
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

            # Wait for the element to be present
            wait = WebDriverWait(self.driver, 10)
            element = wait.until(EC.presence_of_element_located((By.ID, element_id)))

            if field_type == "select":
                # Handle dropdown/select fields
                select = Select(element)
                select.select_by_value(value)
                log.trace(f"Set select field '{field}' to '{value}'")
            elif field_type == "input":
                # Handle text input fields
                element.clear()
                element.send_keys(value)
                log.trace(f"Set input field '{field}' to '{value}'")
            elif field_type == "textarea":
                # Handle textarea fields
                element.clear()
                element.send_keys(value)
                log.trace(f"Set textarea field '{field}' to '{value}'")
            elif field_type == "checkbox":
                # Handle checkbox fields
                if value.lower() in ["true", "yes", "1", "checked"]:
                    if not element.is_selected():
                        element.click()
                    log.trace(f"Checked checkbox field '{field}'")
                else:
                    if element.is_selected():
                        element.click()
                    log.trace(f"Unchecked checkbox field '{field}'")

        except Exception as e:
            log.error(f"Failed to set field '{field}' to '{value}': {e}")
            raise AssertionError(f"Failed to set field '{field}' to '{value}': {e}")

    def create(self):
        """Create the artifact and close the modal."""
        self.submit_button.click()
        return self.clear()

    def save(self):
        submit_button = Button("submit", None, None)
        submit_button.click()
        self.clear()

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
            # Wait for the status field to be present
            wait = WebDriverWait(self.driver, 10)
            element = wait.until(EC.presence_of_element_located((By.ID, "artifactStatus")))
            
            # Get the selected option value
            select = Select(element)
            selected_option = select.first_selected_option
            return selected_option.get_attribute("value")
        except Exception as e:
            log.error(f"Failed to get status field value: {e}")
            return None
