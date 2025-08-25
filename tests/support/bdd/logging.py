"""
Logging configuration for tests.

This module:
 - defines a TRACE level
 - configures the root logger to write ALL messages to a unique logfile at logs/<uuid>.log
 - also writes to console (StreamHandler)
 - exposes `logger` for module imports
 - exposes `LOGFILE_PATH` with the created logfile path (Path object)
"""

import logging
import os
import uuid
from pathlib import Path

# Define custom TRACE level (15) - between DEBUG (10) and INFO (20)
TRACE = 15
logging.addLevelName(TRACE, "TRACE")


def trace(self, message, *args, **kwargs):
    """Add trace method to logger if it doesn't exist."""
    if self.isEnabledFor(TRACE):
        self._log(TRACE, message, args, **kwargs)


# Add trace method to Logger class if it doesn't exist
if not hasattr(logging.Logger, "trace"):
    logging.Logger.trace = trace


def configure_logging():
    """
    Configure logging:
    - Determine level from PYTHON_LOG_LEVEL (defaults to INFO)
    - Create logs/ directory at repository root and a file logs/<uuid>.log
    - Attach a FileHandler to the root logger so all logs are written there
    - Attach a StreamHandler for console output
    - Reduce verbosity for some third-party loggers
    Returns the module logger (logging.getLogger(__name__))
    """
    # Determine log level
    log_level_str = os.getenv("PYTHON_LOG_LEVEL", "INFO").upper()

    level_map = {
        "TRACE": TRACE,
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }

    if log_level_str not in level_map:
        log_level_str = "INFO"

    level = level_map[log_level_str]

    # Compute repository root and logs directory
    # logging.py is at tests/support/bdd/
    # go up 3 levels to reach repository root
    repo_root = Path(__file__).resolve().parents[3]
    logs_dir = repo_root / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    # Create unique logfile name
    logfile_path = logs_dir / f"{uuid.uuid4()}.log"

    # Configure root logger: remove existing handlers to avoid duplicates.
    # Set root level to TRACE so handlers control what is emitted (handlers will filter).
    root = logging.getLogger()
    root.setLevel(logging.WARNING)

    # Remove existing handlers added by other code (if any)
    for h in list(root.handlers):
        root.removeHandler(h)

    # Formatter with timestamp
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s:%(name)s:%(message)s", "%Y-%m-%d %H:%M:%S"
    )

    # File handler: write logs to the logfile.
    # Use the configured 'level' (from PYTHON_LOG_LEVEL) so file captures the requested verbosity.
    fh = logging.FileHandler(logfile_path, encoding="utf-8")
    fh.setLevel(level)
    fh.setFormatter(formatter)
    root.addHandler(fh)

    # Stream handler: console output should only show WARNINGS and above.
    # This ensures INFO (and lower like DEBUG/TRACE) are recorded in the logfile but not printed to console.
    sh = logging.StreamHandler()
    sh.setLevel(logging.WARNING)
    sh.setFormatter(formatter)
    root.addHandler(sh)

    # Reduce verbosity for noisy third-party libs and remove any direct StreamHandlers.
    # Ensure INFO and below are only written to the logfile, and not printed to console.
    noisy_loggers = ["selenium", "urllib3", "requests", "werkzeug", "flask", "iflow", "radish"]
    for nl in noisy_loggers:
        l = logging.getLogger(nl)
        l.setLevel(logging.WARNING)
        # Remove StreamHandlers attached directly to these loggers so they won't print INFO to console
        for h in list(l.handlers):
            if isinstance(h, logging.StreamHandler):
                l.removeHandler(h)
        # Make sure messages propagate to root so they end up in the logfile and are subject
        # to the root StreamHandler (which is set to WARNING).
        l.propagate = True

    # Also sanitize any other loggers which might have been created before configuration:
    for lname, logger_obj in list(logging.root.manager.loggerDict.items()):
        try:
            if isinstance(logger_obj, logging.PlaceHolder):
                continue
        except Exception:
            # If logger_obj is not a PlaceHolder object or inspection fails, skip
            pass
        lobj = logging.getLogger(lname)
        for h in list(lobj.handlers):
            if isinstance(h, logging.StreamHandler):
                lobj.removeHandler(h)
        lobj.propagate = True

    # Make logfile path available to callers
    global LOGFILE_PATH
    LOGFILE_PATH = logfile_path

    # Return module logger
    return logging.getLogger(__name__)


# Initialize logger and export logfile path
logger = configure_logging()
# Export LOGFILE_PATH variable for other modules or tests to inspect
try:
    LOGFILE_PATH  # type: ignore[name-defined]
except NameError:
    LOGFILE_PATH = None
