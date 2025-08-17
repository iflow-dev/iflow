"""
Git-based database for storing and managing artifacts.

All artifacts are stored in a flat structure within a git repository,
using 5-digit sequential numbering for unique identification across all types.
"""

import os
import json
from typing import List, Optional, Dict, Any
from pathlib import Path
import git
from core import Artifact, ArtifactType


class GitDatabase:
    """
    Git-based database for storing artifacts with full history tracking.
    
    All artifacts are stored in a flat structure using 5-digit sequential
    numbering for unique identification across all artifact types.
    """
    
    def __init__(self, repo_path: str = ".iflow"):
        """
        Initialize the git database.
        
        Args:
            repo_path: Path to the git repository for storing artifacts
        """
        self.repo_path = Path(repo_path)
        self.artifacts_dir = self.repo_path / "artifacts"
        self._init_repo()
    
    def _init_repo(self) -> None:
        """Initialize the git repository and artifacts directory."""
        try:
            if not self.repo_path.exists():
                self.repo_path.mkdir(parents=True)
                self.repo = git.Repo.init(self.repo_path)
            else:
                self.repo = git.Repo(self.repo_path)
            
            if not self.artifacts_dir.exists():
                self.artifacts_dir.mkdir()
                
        except git.InvalidGitRepositoryError:
            # If the directory exists but isn't a git repo, reinitialize
            import shutil
            shutil.rmtree(self.repo_path)
            self.repo_path.mkdir(parents=True)
            self.repo = git.Repo.init(self.repo_path)
            self.artifacts_dir.mkdir()
    
    def _get_next_artifact_number(self) -> str:
        """
        Get the next available 5-digit number for artifacts.
        
        Returns:
            Next available 5-digit number as string (e.g., "00001")
        """
        if not self.artifacts_dir.exists():
            return "00001"
        
        # Find the highest existing number across all artifacts
        existing_numbers = []
        for file_path in self.artifacts_dir.glob("*.yaml"):
            filename = file_path.stem  # Remove .yaml extension
            if filename.isdigit() and len(filename) <= 5:
                existing_numbers.append(int(filename))
        
        if not existing_numbers:
            return "00001"
        
        next_number = max(existing_numbers) + 1
        return f"{next_number:05d}"  # Format as 5-digit string
    
    def _get_artifact_path(self, artifact_number: str) -> Path:
        """
        Get the file path for an artifact.
        
        Args:
            artifact_number: The 5-digit number
            
        Returns:
            Path to the artifact file
        """
        return self.artifacts_dir / f"{artifact_number}.yaml"
    
    def _get_repo_relative_path(self, artifact_number: str) -> str:
        """
        Get the repository-relative path for an artifact (for Git operations).
        
        Args:
            artifact_number: The 5-digit number
            
        Returns:
            String path relative to repository root (e.g., "artifacts/00001.yaml")
        """
        return f"artifacts/{artifact_number}.yaml"
    
    def save_artifact(self, artifact: Artifact) -> None:
        """
        Save an artifact to the database.
        
        Args:
            artifact: The artifact to save
        """
        # If artifact doesn't have a number, generate one
        if '/' not in artifact.artifact_id:
            if artifact.artifact_id == "00000":  # Placeholder ID
                # Generate new ID for new artifacts
                artifact_number = self._get_next_artifact_number()
                artifact.artifact_id = artifact_number
            else:
                # Use existing ID for updates
                artifact_number = artifact.artifact_id
        else:
            # Extract number from existing ID (for backward compatibility)
            artifact_number = artifact.artifact_id.split('/')[-1]
        
        # Create file path
        file_path = self._get_artifact_path(artifact_number)
        
        # Check if this is an update or new artifact
        is_update = file_path.exists()
        
        # Write artifact to file
        with open(file_path, 'w') as f:
            content = artifact.to_yaml()
            f.write(content)
            f.flush()  # Ensure data is written to disk
            os.fsync(f.fileno())  # Force sync to disk
        
        # Verify file exists before adding to git
        if not file_path.exists():
            raise RuntimeError(f"Failed to create file: {file_path}")
        
        # Add to git and commit
        # Use repository-relative path for Git operations
        git_file_path = self._get_repo_relative_path(artifact_number)
        
        # Add to git and commit
        # Use repository-relative path for Git operations
        git_file_path = self._get_repo_relative_path(artifact_number)
        
        self.repo.index.add([git_file_path])
        
        # Use appropriate commit message
        if is_update:
            commit_message = f"Update {artifact.type.value}: {artifact.summary}"
        else:
            commit_message = f"Add {artifact.type.value}: {artifact.summary}"
        
        self.repo.index.commit(commit_message)
    
    def get_artifact(self, artifact_id: str) -> Optional[Artifact]:
        """
        Retrieve an artifact by ID.
        
        Args:
            artifact_id: The unique identifier of the artifact (5-digit number)
            
        Returns:
            The artifact if found, None otherwise
        """
        # Handle both old format (type/number) and new format (number only)
        if '/' in artifact_id:
            # Old format: extract just the number
            artifact_number = artifact_id.split('/')[-1]
        else:
            # New format: use the ID directly
            artifact_number = artifact_id
        
        file_path = self._get_artifact_path(artifact_number)
        
        if not file_path.exists():
            return None
        
        try:
            with open(file_path, 'r') as f:
                yaml_content = f.read()
            return Artifact.from_yaml(yaml_content)
        except Exception as e:
            print(f"Error reading artifact {artifact_id}: {e}")
            return None
    
    def list_artifacts(self, artifact_type: Optional[ArtifactType] = None) -> List[Artifact]:
        """
        List all artifacts, optionally filtered by type.
        
        Args:
            artifact_type: Optional filter by artifact type
            
        Returns:
            List of artifacts matching the criteria
        """
        artifacts = []
        
        # List all artifacts from the flat directory
        for file_path in self.artifacts_dir.glob("*.yaml"):
            try:
                with open(file_path, 'r') as f:
                    yaml_content = f.read()
                artifact = Artifact.from_yaml(yaml_content)
                
                # Apply type filter if specified
                if artifact_type is None or artifact.type == artifact_type:
                    artifacts.append(artifact)
                    
            except Exception as e:
                print(f"Error reading artifact from {file_path}: {e}")
                continue
        
        # Sort by creation date (newest first)
        artifacts.sort(key=lambda x: x.created_at, reverse=True)
        return artifacts
    
    def update_artifact(self, artifact: Artifact) -> None:
        """
        Update an existing artifact.
        
        Args:
            artifact: The updated artifact
        """
        if not self.get_artifact(artifact.artifact_id):
            raise ValueError(f"Artifact {artifact.artifact_id} does not exist")
        
        self.save_artifact(artifact)
    
    def delete_artifact(self, artifact_id: str) -> None:
        """
        Delete an artifact from the database.
        
        Args:
            artifact_id: The unique identifier of the artifact (5-digit number)
        """
        # Handle both old format (type/number) and new format (number only)
        if '/' in artifact_id:
            # Old format: extract just the number
            artifact_number = artifact_id.split('/')[-1]
        else:
            # New format: use the ID directly
            artifact_number = artifact_id
        
        file_path = self._get_artifact_path(artifact_number)
        
        if not file_path.exists():
            raise ValueError(f"Artifact {artifact_id} does not exist")
        
        # Remove from git and commit
        # Use repository-relative path for Git operations
        git_file_path = self._get_repo_relative_path(artifact_number)
        self.repo.index.remove([git_file_path])
        
        # Delete the actual file from filesystem
        file_path.unlink()
        
        commit_message = f"Delete artifact: {artifact_id}"
        self.repo.index.commit(commit_message)
    
    def search_artifacts(self, query: str) -> List[Artifact]:
        """
        Search artifacts by text in summary or description.
        
        Args:
            query: Search query string
            
        Returns:
            List of artifacts matching the search query
        """
        query_lower = query.lower()
        matching_artifacts = []
        
        for artifact in self.list_artifacts():
            if (query_lower in artifact.summary.lower() or 
                query_lower in artifact.description.lower()):
                matching_artifacts.append(artifact)
        
        return matching_artifacts
    
    def get_artifact_history(self, artifact_id: str) -> List[Dict[str, Any]]:
        """
        Get the git history for a specific artifact.
        
        Args:
            artifact_id: The unique identifier of the artifact (5-digit number)
            
        Returns:
            List of commit information for the artifact
        """
        # Handle both old format (type/number) and new format (number only)
        if '/' in artifact_id:
            # Old format: extract just the number
            artifact_number = artifact_id.split('/')[-1]
        else:
            # New format: use the ID directly
            artifact_number = artifact_id
        
        file_path = self._get_artifact_path(artifact_number)
        
        if not file_path.exists():
            return []
        
        try:
            # Get git log for the specific file
            # Use repository-relative path for Git operations
            git_file_path = self._get_repo_relative_path(artifact_number)
            commits = list(self.repo.iter_commits(paths=git_file_path))
            history = []
            
            for commit in commits:
                history.append({
                    'hash': commit.hexsha,
                    'author': commit.author.name,
                    'date': commit.committed_datetime,
                    'message': commit.message.strip()
                })
            
            return history
        except Exception as e:
            print(f"Error getting history for artifact {artifact_id}: {e}")
            return []
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get database statistics.
        
        Returns:
            Dictionary containing database statistics
        """
        all_artifacts = self.list_artifacts()
        
        stats = {
            'total_artifacts': len(all_artifacts),
            'by_type': {},
            'total_commits': len(list(self.repo.iter_commits())),
            'last_commit': None
        }
        
        # Count by type
        for artifact in all_artifacts:
            artifact_type = artifact.type.value
            stats['by_type'][artifact_type] = stats['by_type'].get(artifact_type, 0) + 1
        
        # Get last commit info
        try:
            last_commit = self.repo.head.commit
            stats['last_commit'] = {
                'hash': last_commit.hexsha,
                'author': last_commit.author.name,
                'date': last_commit.committed_datetime,
                'message': last_commit.message.strip()
            }
        except Exception:
            pass
        
        return stats
    
    @property
    def config(self) -> Dict[str, Any]:
        """
        Get the configuration from the config.yaml file in the repository.
        
        Returns:
            Dictionary containing the configuration data
        """
        import yaml
        
        config_path = self.repo_path / "config.yaml"
        
        if not config_path.exists():
            # Return default configuration if file doesn't exist
            return self._get_default_config()
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                return config if config else self._get_default_config()
        except Exception as e:
            print(f"Error loading config from {config_path}: {e}")
            # Return default configuration on error
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """
        Get default configuration when config.yaml is not available.
        
        Returns:
            Dictionary containing default configuration
        """
        return {
            "project": {
                "name": "iflow",
                "description": "Git-based artifact management system",
                "version": "1.0.0"
            },
            "work_item_types": [
                {
                    "id": "requirement",
                    "name": "Requirement",
                    "description": "Functional or non-functional requirements",
                    "color": "#60A5FA",
                    "icon": "ion-flash-outline"
                },
                {
                    "id": "task",
                    "name": "Task",
                    "description": "Work items that need to be completed",
                    "color": "#34D399",
                    "icon": "✅"
                },
                {
                    "id": "bug",
                    "name": "Bug",
                    "description": "Issues or defects that need to be fixed",
                    "color": "#F87171",
                    "icon": "🐛"
                },
                {
                    "id": "aspect",
                    "name": "Aspect",
                    "description": "Cross-cutting concerns and quality attributes",
                    "color": "#A78BFA",
                    "icon": "🔍"
                }
            ],
            "repository": {
                "artifacts_dir": "artifacts",
                "backup_dir": "artifacts_backup",
                "max_artifacts": 99999
            },
            "artifact_statuses": [
                {
                    "id": "open",
                    "name": "Open",
                    "description": "Artifact is open and ready for work",
                    "color": "#10B981",
                    "icon": "🟢"
                },
                {
                    "id": "in_progress",
                    "name": "In Progress",
                    "description": "Work has started on this artifact",
                    "color": "#F59E0B",
                    "icon": "🟡"
                },
                {
                    "id": "done",
                    "name": "Done",
                    "description": "Artifact is completed",
                    "color": "#3B82F6",
                    "icon": "✅"
                },
                {
                    "id": "blocked",
                    "name": "Blocked",
                    "description": "Artifact is blocked and cannot proceed",
                    "color": "#EF4444",
                    "icon": "🔴"
                }
            ],
            "ui": {
                "default_view": "all",
                "items_per_page": 20,
                "enable_search": True,
                "enable_filters": True
            }
        }
