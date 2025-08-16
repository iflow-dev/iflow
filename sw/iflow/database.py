"""
Git-based database for storing and managing artifacts.
"""

import os
import json
from typing import List, Optional, Dict, Any
from pathlib import Path
import git
from .core import Artifact, ArtifactType


class GitDatabase:
    """
    Git-based database for storing artifacts with full history tracking.
    
    All artifacts are stored in a flat structure within a git repository,
    allowing for complete version control and history tracking.
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
    
    def save_artifact(self, artifact: Artifact) -> None:
        """
        Save an artifact to the database.
        
        Args:
            artifact: The artifact to save
        """
        # Create filename based on artifact ID and type
        filename = f"{artifact.artifact_id}.yaml"
        file_path = self.artifacts_dir / filename
        
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
        # Use absolute path for git operations
        git_file_path = str(file_path.absolute())
        
        self.repo.index.add([git_file_path])
        commit_message = f"Add {artifact.type.value}: {artifact.summary}"
        self.repo.index.commit(commit_message)
    
    def get_artifact(self, artifact_id: str) -> Optional[Artifact]:
        """
        Retrieve an artifact by ID.
        
        Args:
            artifact_id: The unique identifier of the artifact
            
        Returns:
            The artifact if found, None otherwise
        """
        filename = f"{artifact_id}.yaml"
        file_path = self.artifacts_dir / filename
        
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
        
        for file_path in self.artifacts_dir.glob("*.yaml"):
            try:
                with open(file_path, 'r') as f:
                    yaml_content = f.read()
                artifact = Artifact.from_yaml(yaml_content)
                
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
            artifact_id: The unique identifier of the artifact to delete
        """
        filename = f"{artifact_id}.yaml"
        file_path = self.artifacts_dir / filename
        
        if not file_path.exists():
            raise ValueError(f"Artifact {artifact_id} does not exist")
        
        # Remove from git and commit
        self.repo.index.remove([str(file_path)])
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
            artifact_id: The unique identifier of the artifact
            
        Returns:
            List of commit information for the artifact
        """
        filename = f"{artifact_id}.yaml"
        file_path = self.artifacts_dir / filename
        
        if not file_path.exists():
            return []
        
        try:
            # Get git log for the specific file
            commits = list(self.repo.iter_commits(paths=str(file_path)))
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
