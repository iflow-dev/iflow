"""
Terrain file for radish BDD tests.
This file is automatically loaded by radish and sets up the test environment.
"""

# Import all step definition modules
from steps import (
    artifact_creation_steps,
    artifact_flags_steps,
    artifact_steps,
    dropdown_selection_steps,
    edit_button_steps,
    simple_steps,
    status_filtering_steps,
    # toolbar_refresh_steps,  # Temporarily commented out due to duplicate step definition
    version_display_steps,
    artifacts
)

# Import support modules
from support import world, hooks
