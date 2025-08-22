"""
World configuration for radish BDD tests.
This file sets up shared state and configuration.
All hooks are now in hooks.py for better organization.
"""

from radish import world
import os
from bdd.logging_config import logger as log

# ============================================================================
# WORLD CONFIGURATION
# ============================================================================

def initialize_world():
    """Initialize world configuration and shared state."""
    log.trace("Starting world configuration initialization...")
    
    # Base URL will be set by hooks.py during @before.all
    # ChromeDriver will be initialized by hooks.py during @before.all
    
    # Any additional world configuration can go here
    log.trace("World configuration initialization completed")

# ============================================================================
# SHARED STATE ACCESSORS
# ============================================================================

def get_driver():
    """Get the current ChromeDriver instance."""
    log.trace("Getting ChromeDriver instance from world")
    if hasattr(world, 'driver') and world.driver:
        log.trace("ChromeDriver found in world")
        return world.driver
    else:
        log.trace("ChromeDriver not found in world")
        raise RuntimeError("ChromeDriver not initialized. Make sure hooks.py is loaded.")

def get_base_url():
    """Get the current base URL."""
    log.trace("Getting base URL from world")
    if hasattr(world, 'base_url') and world.base_url:
        log.trace(f"Base URL found in world: {world.base_url}")
        return world.base_url
    else:
        log.trace("Base URL not found in world")
        raise RuntimeError("Base URL not set. Make sure hooks.py is loaded.")

def get_current_scenario():
    """Get current scenario information if available."""
    log.trace("Getting current scenario from world")
    if hasattr(world, 'current_scenario'):
        log.trace(f"Current scenario found: {world.current_scenario}")
        return world.current_scenario
    log.trace("No current scenario found in world")
    return None

# ============================================================================
# UTILITY FUNCTIONS FOR WORLD STATE
# ============================================================================

def is_driver_ready():
    """Check if ChromeDriver is ready for use."""
    log.trace("Checking if ChromeDriver is ready")
    driver_ready = hasattr(world, 'driver') and world.driver is not None
    log.trace(f"ChromeDriver ready: {driver_ready}")
    return driver_ready

def is_base_url_set():
    """Check if base URL is configured."""
    log.trace("Checking if base URL is set")
    base_url_set = hasattr(world, 'base_url') and world.base_url is not None
    log.trace(f"Base URL set: {base_url_set}")
    return base_url_set

def log_world_state():
    """Log current world state for debugging."""
    log.trace("=== Starting World State Log ===")
    log.trace(f"Driver ready: {is_driver_ready()}")
    log.trace(f"Base URL set: {is_base_url_set()}")
    if is_base_url_set():
        log.trace(f"Base URL: {get_base_url()}")
    log.trace("=== World State Log Complete ===")
