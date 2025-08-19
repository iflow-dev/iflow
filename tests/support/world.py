"""
World configuration for radish BDD tests.
This file sets up shared state and configuration.
All hooks are now in hooks.py for better organization.
"""

from radish import world
import os
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

# ============================================================================
# WORLD CONFIGURATION
# ============================================================================

def initialize_world():
    """Initialize world configuration and shared state."""
    log.debug("Initializing world configuration...")
    
    # Base URL will be set by hooks.py during @before.all
    # ChromeDriver will be initialized by hooks.py during @before.all
    
    # Any additional world configuration can go here
    log.debug("World configuration initialized")

# ============================================================================
# SHARED STATE ACCESSORS
# ============================================================================

def get_driver():
    """Get the current ChromeDriver instance."""
    if hasattr(world, 'driver') and world.driver:
        return world.driver
    else:
        raise RuntimeError("ChromeDriver not initialized. Make sure hooks.py is loaded.")

def get_base_url():
    """Get the current base URL."""
    if hasattr(world, 'base_url') and world.base_url:
        return world.base_url
    else:
        raise RuntimeError("Base URL not set. Make sure hooks.py is loaded.")

def get_current_scenario():
    """Get current scenario information if available."""
    if hasattr(world, 'current_scenario'):
        return world.current_scenario
    return None

# ============================================================================
# UTILITY FUNCTIONS FOR WORLD STATE
# ============================================================================

def is_driver_ready():
    """Check if ChromeDriver is ready for use."""
    return hasattr(world, 'driver') and world.driver is not None

def is_base_url_set():
    """Check if base URL is configured."""
    return hasattr(world, 'base_url') and world.base_url is not None

def log_world_state():
    """Log current world state for debugging."""
    log.debug("=== World State ===")
    log.debug(f"Driver ready: {is_driver_ready()}")
    log.debug(f"Base URL set: {is_base_url_set()}")
    if is_base_url_set():
        log.debug(f"Base URL: {get_base_url()}")
    log.debug("==================")
