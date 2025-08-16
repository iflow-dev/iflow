"""
Tests for the core module.
"""

import pytest
from datetime import datetime
from iflow.core import Artifact, ArtifactType


class TestArtifactType:
    """Test ArtifactType enum."""
    
    def test_artifact_type_values(self):
        """Test that all artifact types have expected values."""
        assert ArtifactType.REQUIREMENT.value == "requirement"
        assert ArtifactType.TASK.value == "task"
        assert ArtifactType.TEST_CASE.value == "test_case"
        assert ArtifactType.ISSUE.value == "issue"
        assert ArtifactType.BUG.value == "bug"
        assert ArtifactType.FEATURE.value == "feature"
        assert ArtifactType.STORY.value == "story"
    
    def test_artifact_type_count(self):
        """Test that we have the expected number of artifact types."""
        assert len(ArtifactType) == 7


class TestArtifact:
    """Test Artifact class."""
    
    def test_artifact_creation(self):
        """Test basic artifact creation."""
        artifact = Artifact(
            artifact_type=ArtifactType.REQUIREMENT,
            summary="Test requirement",
            description="Test description"
        )
        
        assert artifact.type == ArtifactType.REQUIREMENT
        assert artifact.summary == "Test requirement"
        assert artifact.description == "Test description"
        assert artifact.artifact_id is not None
        assert artifact.created_at is not None
        assert artifact.updated_at is not None
        assert artifact.metadata == {}
    
    def test_artifact_with_custom_id(self):
        """Test artifact creation with custom ID."""
        custom_id = "REQ-001"
        artifact = Artifact(
            artifact_type=ArtifactType.REQUIREMENT,
            summary="Test requirement",
            artifact_id=custom_id
        )
        
        assert artifact.artifact_id == custom_id
    
    def test_artifact_with_custom_dates(self):
        """Test artifact creation with custom dates."""
        custom_date = datetime(2023, 1, 1, 12, 0, 0)
        artifact = Artifact(
            artifact_type=ArtifactType.TASK,
            summary="Test task",
            created_at=custom_date,
            updated_at=custom_date
        )
        
        assert artifact.created_at == custom_date
        assert artifact.updated_at == custom_date
    
    def test_artifact_with_metadata(self):
        """Test artifact creation with metadata."""
        metadata = {"priority": "high", "assignee": "john"}
        artifact = Artifact(
            artifact_type=ArtifactType.BUG,
            summary="Test bug",
            metadata=metadata
        )
        
        assert artifact.metadata == metadata
    
    def test_artifact_to_dict(self):
        """Test artifact to dictionary conversion."""
        artifact = Artifact(
            artifact_type=ArtifactType.FEATURE,
            summary="Test feature",
            description="Test description"
        )
        
        data = artifact.to_dict()
        
        assert "artifact" in data
        artifact_data = data["artifact"]
        assert artifact_data["type"] == "feature"
        assert artifact_data["summary"] == "Test feature"
        assert artifact_data["description"] == "Test description"
        assert "id" in artifact_data
        assert "created_at" in artifact_data
        assert "updated_at" in artifact_data
        assert "metadata" in artifact_data
    
    def test_artifact_to_yaml(self):
        """Test artifact to YAML conversion."""
        artifact = Artifact(
            artifact_type=ArtifactType.STORY,
            summary="Test story"
        )
        
        yaml_str = artifact.to_yaml()
        
        assert "artifact:" in yaml_str
        assert "type: story" in yaml_str
        assert "summary: Test story" in yaml_str
    
    def test_artifact_from_dict(self):
        """Test artifact creation from dictionary."""
        data = {
            "artifact": {
                "id": "TEST-001",
                "type": "requirement",
                "summary": "Test requirement",
                "description": "Test description",
                "created_at": "2023-01-01T12:00:00",
                "updated_at": "2023-01-01T12:00:00",
                "metadata": {"priority": "high"}
            }
        }
        
        artifact = Artifact.from_dict(data)
        
        assert artifact.artifact_id == "TEST-001"
        assert artifact.type == ArtifactType.REQUIREMENT
        assert artifact.summary == "Test requirement"
        assert artifact.description == "Test description"
        assert artifact.metadata == {"priority": "high"}
    
    def test_artifact_from_yaml(self):
        """Test artifact creation from YAML."""
        yaml_str = """
artifact:
    id: YAML-001
    type: task
    summary: Test task
    description: Test description
    created_at: 2023-01-01T12:00:00
    updated_at: 2023-01-01T12:00:00
    metadata: {}
        """
        
        artifact = Artifact.from_yaml(yaml_str)
        
        assert artifact.artifact_id == "YAML-001"
        assert artifact.type == ArtifactType.TASK
        assert artifact.summary == "Test task"
    
    def test_artifact_update(self):
        """Test artifact update functionality."""
        artifact = Artifact(
            artifact_type=ArtifactType.ISSUE,
            summary="Original summary"
        )
        
        original_updated_at = artifact.updated_at
        
        # Update the artifact
        artifact.update(summary="Updated summary", description="New description")
        
        assert artifact.summary == "Updated summary"
        assert artifact.description == "New description"
        assert artifact.updated_at > original_updated_at
    
    def test_artifact_string_representation(self):
        """Test artifact string representation."""
        artifact = Artifact(
            artifact_type=ArtifactType.BUG,
            summary="Test bug",
            artifact_id="BUG-001"
        )
        
        str_repr = str(artifact)
        assert "bug: Test bug" in str_repr
        assert "BUG-001" in str_repr
    
    def test_artifact_repr_representation(self):
        """Test artifact repr representation."""
        artifact = Artifact(
            artifact_type=ArtifactType.TEST_CASE,
            summary="Test case",
            artifact_id="TC-001"
        )
        
        repr_str = repr(artifact)
        assert "Artifact(" in repr_str
        assert "type=test_case" in repr_str
        assert "summary='Test case'" in repr_str
        assert "id='TC-001'" in repr_str
