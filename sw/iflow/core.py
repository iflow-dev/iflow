"""
Core classes for iflow artifacts.
"""

from typing import Dict, Any, Optional
import yaml
from datetime import datetime


class ArtifactType:
    """Simple artifact type wrapper that can be any string value."""
    
    def __init__(self, value: str):
        self.value = value
    
    def __eq__(self, other):
        if isinstance(other, ArtifactType):
            return self.value == other.value
        elif isinstance(other, str):
            return self.value == other
        return False
    
    def __hash__(self):
        return hash(self.value)
    
    def __str__(self):
        return self.value
    
    def __repr__(self):
        return f"ArtifactType('{self.value}')"


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
        metadata: Optional[Dict[str, Any]] = None,
        flagged: bool = False
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
        self.flagged = flagged
    
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
                "metadata": self.metadata,
                "flagged": self.flagged
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
            created_at=datetime.fromisoformat(artifact_data["created_at"]).replace(tzinfo=None),
            updated_at=datetime.fromisoformat(artifact_data["updated_at"]).replace(tzinfo=None),
            metadata=artifact_data.get("metadata", {}),
            flagged=artifact_data.get("flagged", False)
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
