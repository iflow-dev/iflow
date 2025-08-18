"""
iflow - A tool for managing project artifacts like requirements, tasks, test cases, and issues.

iflow is a Python package that provides a web-based application using pywebview
for managing project artifacts with git-based storage and YAML-like structure.
"""

__version__ = "0.3.1"
__author__ = "iflow team"

from .core import Artifact, ArtifactType
from .database import GitDatabase
from .app import IFlowApp

__all__ = ["Artifact", "ArtifactType", "GitDatabase", "IFlowApp"]
