"""
iflow - Git-based artifact management system
"""

__version__ = "0.3.2"
__author__ = "iflow team"

from .core import Artifact, ArtifactType
from .database import GitDatabase
from .app import IFlowApp

__all__ = ["Artifact", "ArtifactType", "GitDatabase", "IFlowApp"]
