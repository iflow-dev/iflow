"""
Logging configuration for tests.
This file provides a centralized way to control logging levels.
"""

import logging
import os

def configure_logging():
    """Configure logging level based on environment variable or default to INFO."""
    log_level = os.getenv('PYTHON_LOG_LEVEL', 'INFO').upper()
    
    # Map string levels to logging constants
    level_map = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }
    
    # Default to INFO if invalid level specified
    if log_level not in level_map:
        log_level = 'INFO'
    
    # Configure basic logging
    logging.basicConfig(
        level=level_map[log_level],
        format='%(levelname)s:%(name)s:%(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Set specific logger levels for verbose libraries
    logging.getLogger('selenium').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('requests').setLevel(logging.WARNING)
    
    return logging.getLogger(__name__)

# Create a logger instance
logger = configure_logging()
