"""
iflow - Project Artifact Manager

A Git-based project artifact management system that stores requirements,
tasks, test cases, and other project artifacts in a version-controlled
repository.
"""

__version__ = "0.4.0a1"
__author__ = "iflow team"

from .core import Artifact, ArtifactType
from .database import GitDatabase
from .app import IFlowApp

__all__ = ["Artifact", "ArtifactType", "GitDatabase", "IFlowApp"]
