"""
API module for iflow application.

This module contains the APIProxy class that handles communication between
the frontend and backend, providing a clean interface for artifact management.
"""

from typing import Dict, Any, Optional, List
from .core import Artifact, ArtifactType


class APIProxy:
    """
    API proxy class for communication between the frontend and backend.
    
    This class provides methods that can be called from the JavaScript frontend
    to interact with the artifact database, ensuring proper isolation from
    pywebview serialization issues.
    """
    
    def __init__(self, app_instance):
        """
        Initialize the API proxy with an app instance.
        
        Args:
            app_instance: The main application instance containing the database
        """
        self._app = app_instance
    
    def list_artifacts(self, artifact_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List all artifacts, optionally filtered by type.
        
        Args:
            artifact_type: Optional artifact type filter
            
        Returns:
            List of artifacts as dictionaries
        """
        try:
            print(f"list_artifacts called with type: {artifact_type}")
            if artifact_type:
                artifact_type_enum = ArtifactType(artifact_type)
                artifacts = self._app.db.list_artifacts(artifact_type_enum)
            else:
                artifacts = self._app.db.list_artifacts()
            
            print(f"Found {len(artifacts)} artifacts")
            # Convert to dictionaries for JSON serialization
            result = [self._app._artifact_to_dict(artifact) for artifact in artifacts]
            print(f"Converted to {len(result)} dictionaries")
            return result
        except Exception as e:
            print(f"Error listing artifacts: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def get_artifact(self, artifact_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific artifact by ID.
        
        Args:
            artifact_id: The unique identifier of the artifact
            
        Returns:
            The artifact as a dictionary, or None if not found
        """
        try:
            artifact = self._app.db.get_artifact(artifact_id)
            if artifact:
                return self._app._artifact_to_dict(artifact)
            return None
        except Exception as e:
            print(f"Error getting artifact {artifact_id}: {e}")
            return None
    
    def create_artifact(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new artifact.
        
        Args:
            data: Dictionary containing artifact data
            
        Returns:
            The created artifact as a dictionary
        """
        try:
            artifact = Artifact(
                artifact_type=ArtifactType(data['type']),
                summary=data['summary'],
                description=data.get('description', ''),
                artifact_id=data.get('artifact_id')
            )
            
            self._app.db.save_artifact(artifact)
            return self._app._artifact_to_dict(artifact)
        except Exception as e:
            print(f"Error creating artifact: {e}")
            raise e
    
    def update_artifact(self, artifact_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing artifact.
        
        Args:
            artifact_id: The unique identifier of the artifact
            data: Dictionary containing updated artifact data
            
        Returns:
            The updated artifact as a dictionary
        """
        try:
            artifact = self._app.db.get_artifact(artifact_id)
            if not artifact:
                raise ValueError(f"Artifact {artifact_id} not found")
            
            # Update fields
            if 'type' in data:
                artifact.type = ArtifactType(data['type'])
            if 'summary' in data:
                artifact.summary = data['summary']
            if 'description' in data:
                artifact.description = data['description']
            
            # Update timestamp
            artifact.update()
            
            # Save to database
            self._app.db.save_artifact(artifact)
            return self._app._artifact_to_dict(artifact)
        except Exception as e:
            print(f"Error updating artifact {artifact_id}: {e}")
            raise e
    
    def delete_artifact(self, artifact_id: str) -> bool:
        """
        Delete an artifact.
        
        Args:
            artifact_id: The unique identifier of the artifact
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self._app.db.delete_artifact(artifact_id)
            return True
        except Exception as e:
            print(f"Error deleting artifact {artifact_id}: {e}")
            return False
    
    def search_artifacts(self, query: str) -> List[Dict[str, Any]]:
        """
        Search artifacts by text.
        
        Args:
            query: Search query string
            
        Returns:
            List of matching artifacts as dictionaries
        """
        try:
            artifacts = self._app.db.search_artifacts(query)
            return [self._app._artifact_to_dict(artifact) for artifact in artifacts]
        except Exception as e:
            print(f"Error searching artifacts: {e}")
            return []
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get database statistics.
        
        Returns:
            Dictionary containing database statistics
        """
        try:
            stats = self._app.db.get_stats()
            # Ensure all datetime objects are converted to strings for JSON serialization
            if 'last_commit' in stats and stats['last_commit']:
                commit_info = stats['last_commit']
                if hasattr(commit_info, 'get'):
                    # If it's a dict-like object, convert datetime fields
                    if 'date' in commit_info and hasattr(commit_info['date'], 'isoformat'):
                        commit_info['date'] = commit_info['date'].isoformat()
                elif hasattr(commit_info, 'isoformat'):
                    # If it's a datetime object directly
                    stats['last_commit'] = commit_info.isoformat()
            return stats
        except Exception as e:
            print(f"Error getting stats: {e}")
            return {
                'total_artifacts': 0,
                'by_type': {},
                'total_commits': 0,
                'last_commit': None
            }
