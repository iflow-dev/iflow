"""
Configuration management for iflow project.

Handles reading and managing project configuration from config.yaml,
including work item types, repository settings, and UI preferences.
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional
from .core import ArtifactType


class ProjectConfig:
    """Manages project configuration and settings."""
    
    def __init__(self, config_path: str = ".iflow/config.yaml"):
        """
        Initialize the project configuration.
        
        Args:
            config_path: Path to the configuration file
        """
        self.config_path = Path(config_path)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            return self._get_default_config()
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                return self._merge_with_defaults(config)
        except Exception as e:
            print(f"Warning: Could not load config from {self.config_path}: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration if no config file exists."""
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
                    "icon": "📋"
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
            "ui": {
                "default_view": "all",
                "items_per_page": 20,
                "enable_search": True,
                "enable_filters": True
            }
        }
    
    def _merge_with_defaults(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Merge loaded config with defaults to ensure all required keys exist."""
        default_config = self._get_default_config()
        
        def merge_dicts(d1: Dict[str, Any], d2: Dict[str, Any]) -> Dict[str, Any]:
            result = d1.copy()
            for key, value in d2.items():
                if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                    result[key] = merge_dicts(result[key], value)
                else:
                    result[key] = value
            return result
        
        return merge_dicts(default_config, config)
    
    def get_project_info(self) -> Dict[str, str]:
        """Get basic project information."""
        return self.config.get("project", {})
    
    def get_work_item_types(self) -> List[Dict[str, Any]]:
        """Get list of available work item types."""
        return self.config.get("work_item_types", [])
    
    def get_work_item_type(self, type_id: str) -> Optional[Dict[str, Any]]:
        """Get specific work item type by ID."""
        for work_type in self.get_work_item_types():
            if work_type.get("id") == type_id:
                return work_type
        return None
    
    def get_work_item_type_names(self) -> List[str]:
        """Get list of work item type names for display."""
        return [wt.get("name", wt.get("id", "")) for wt in self.get_work_item_types()]
    
    def get_work_item_type_ids(self) -> List[str]:
        """Get list of work item type IDs."""
        return [wt.get("id", "") for wt in self.get_work_item_types()]
    
    def get_repository_settings(self) -> Dict[str, Any]:
        """Get repository configuration settings."""
        return self.config.get("repository", {})
    
    def get_ui_settings(self) -> Dict[str, Any]:
        """Get UI configuration settings."""
        return self.config.get("ui", {})
    
    def validate_artifact_type(self, artifact_type: str) -> bool:
        """Validate if an artifact type is supported."""
        return artifact_type in self.get_work_item_type_ids()
    
    def get_artifact_type_display_info(self, artifact_type: str) -> Dict[str, Any]:
        """Get display information for an artifact type (name, color, icon)."""
        type_info = self.get_work_item_type(artifact_type)
        if type_info:
            return {
                "id": type_info.get("id", artifact_type),
                "name": type_info.get("name", artifact_type.title()),
                "color": type_info.get("color", "#6B7280"),
                "icon": type_info.get("icon", "📄")
            }
        return {
            "id": artifact_type,
            "name": artifact_type.title(),
            "color": "#6B7280",
            "icon": "📄"
        }
    
    def reload_config(self) -> None:
        """Reload configuration from file."""
        self.config = self._load_config()
    
    def save_config(self) -> None:
        """Save current configuration to file."""
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f, default_flow_style=False, allow_unicode=True)
        except Exception as e:
            print(f"Error saving config: {e}")


# Global configuration instance
_config_instance: Optional[ProjectConfig] = None


def get_config(config_path: str = ".iflow/config.yaml") -> ProjectConfig:
    """Get global configuration instance."""
    global _config_instance
    if _config_instance is None:
        _config_instance = ProjectConfig(config_path)
    return _config_instance


def reload_config(config_path: str = ".iflow/config.yaml") -> ProjectConfig:
    """Reload global configuration."""
    global _config_instance
    _config_instance = ProjectConfig(config_path)
    return _config_instance
