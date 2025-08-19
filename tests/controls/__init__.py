"""
Control classes for BDD test automation.
This module provides page object pattern classes for interacting with web elements.
"""

import sys
import os
# Add the tests directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import all control classes from their respective modules using absolute imports
from controls.base import ControlBase
from controls.button import Button
from controls.input_field import InputField
from controls.editor import Editor
from controls.modal import Modal
from controls.simple_controls import Title, Navigation, Tile, StatusLine

# Export all classes for backward compatibility
__all__ = [
    'ControlBase',
    'Button', 
    'InputField',
    'Editor',
    'Modal',
    'Title',
    'Navigation',
    'Tile',
    'StatusLine'
]
