"""
Core classes for iflow artifacts.
"""

from enum import Enum
from typing import Dict, Any, Optional
import yaml
from datetime import datetime


class ArtifactType(Enum):
    """Enumeration of supported artifact types."""
    REQUIREMENT = "requirement"
    TASK = "task"
    TEST_CASE = "test_case"
    ISSUE = "issue"
    BUG = "bug"
    FEATURE = "feature"
    STORY = "story"
    ASPECT = "aspect"


class Artifact:
    """
    Represents a project artifact with YAML-like structure.
    
    Artifacts are the core data structure in iflow, containing all project
    information like requirements, tasks, test cases, and issues.
    
    Artifact IDs are now 5-digit sequential identifiers that are unique
    across all artifact types.
    """
    
    def __init__(
        self,
        artifact_type: ArtifactType,
        summary: str,
        description: str = "",
        category: str = "",
        status: str = "open",
        artifact_id: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        # artifact_id will be set by the database when saving
        # It will be a 5-digit number (e.g., "00001")
        self.artifact_id = artifact_id or "00000"  # Placeholder
        self.type = artifact_type
        self.summary = summary
        self.description = description
        self.category = category
        self.status = status
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
        self.metadata = metadata or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert artifact to dictionary representation."""
        return {
            "artifact": {
                "id": self.artifact_id,
                "type": self.type.value,
                "summary": self.summary,
                "description": self.description,
                "category": self.category,
                "status": self.status,
                "created_at": self.created_at.isoformat(),
                "updated_at": self.updated_at.isoformat(),
                "metadata": self.metadata
            }
        }
    
    def to_yaml(self) -> str:
        """Convert artifact to YAML string representation."""
        return yaml.dump(self.to_dict(), default_flow_style=False, sort_keys=False)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Artifact':
        """Create artifact from dictionary representation."""
        artifact_data = data.get("artifact", {})
        return cls(
            artifact_type=ArtifactType(artifact_data["type"]),
            summary=artifact_data["summary"],
            description=artifact_data.get("description", ""),
            category=artifact_data.get("category", ""),
            status=artifact_data.get("status", "open"),
            artifact_id=artifact_data["id"],
            created_at=datetime.fromisoformat(artifact_data["created_at"]),
            updated_at=datetime.fromisoformat(artifact_data["updated_at"]),
            metadata=artifact_data.get("metadata", {})
        )
    
    @classmethod
    def from_yaml(cls, yaml_str: str) -> 'Artifact':
        """Create artifact from YAML string."""
        data = yaml.safe_load(yaml_str)
        return cls.from_dict(data)
    
    def update(self, **kwargs) -> None:
        """Update artifact fields."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now()
    
    def __str__(self) -> str:
        return f"{self.type.value}: {self.summary} (ID: {self.artifact_id})"
    
    def __repr__(self) -> str:
        return f"Artifact(type={self.type.value}, summary='{self.summary}', id='{self.artifact_id}')"
