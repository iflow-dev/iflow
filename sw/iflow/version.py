"""
Centralized version management for iflow.

This module provides a single source of truth for the application version,
reading it from the project's __init__.py file rather than from database configuration.
"""

import os
import sys
from pathlib import Path
from importlib import metadata

def get_version() -> str:
    """
    Get the current version of iflow.
    
    This function reads the version from the installed package metadata,
    falling back to the __version__ attribute from the iflow module.
    
    Returns:
        str: The current version string (e.g., "0.3.0")
    """
    try:
        # Try to get version from installed package metadata first
        return metadata.version("iflow")
    except metadata.PackageNotFoundError:
        # Fallback to reading from __init__.py if package is not installed
        try:
            from . import __version__
            return __version__
        except ImportError:
            # Final fallback: try to read from __init__.py file directly
            return _read_version_from_file()

def _read_version_from_file() -> str:
    """
    Read version from __init__.py file as a last resort.
    
    Returns:
        str: The version string from __init__.py
    """
    try:
        # Get the path to the iflow package
        current_file = Path(__file__)
        init_file = current_file.parent / "__init__.py"
        
        if init_file.exists():
            with open(init_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # Look for __version__ = "x.y.z" pattern
                import re
                match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
                if match:
                    return match.group(1)
    except Exception as e:
        print(f"Warning: Could not read version from file: {e}")
    
    # Ultimate fallback
    return "0.0.0"

def get_version_info() -> dict:
    """
    Get comprehensive version information.
    
    Returns:
        dict: Dictionary containing version information
    """
    version = get_version()
    return {
        "version": version,
        "full_version": f"v{version}",
        "source": "project_repository"
    }

# For backward compatibility
__version__ = get_version()

