"""
Main application module for iflow using pywebview.
"""

import webview
import json
import os
from typing import List, Dict, Any, Optional
from .core import Artifact, ArtifactType
from .database import GitDatabase


class IFlowApp:
    """
    Main iflow application using pywebview for the user interface.
    
    This class provides the web-based interface for managing project artifacts
    and handles communication between the frontend and backend.
    """
    
    def __init__(self, database_path: str = ".iflow"):
        """
        Initialize the iflow application.
        
        Args:
            database_path: Path to the git database
        """
        self.db = GitDatabase(database_path)
        self.window = None
        # Create API functions without exposing the database object directly
        self.api = self._create_api_proxy()
    
    def run(self, title: str = "iflow - Project Artifact Manager"):
        """
        Run the iflow application.
        
        Args:
            title: Window title for the application
        """
        # Get the path to the HTML file
        html_path = os.path.join(os.path.dirname(__file__), 'static', 'index.html')
        
        # Verify the file exists
        if not os.path.exists(html_path):
            print(f"Error: HTML file not found at {html_path}")
            # Fallback to a simple HTML interface
            html_content = """
            <html>
            <body>
                <h1>iflow - Project Artifact Manager</h1>
                <p>Error: Could not load interface file.</p>
                <p>Expected location: {}</p>
            </body>
            </html>
            """.format(html_path)
            
            self.window = webview.create_window(
                title=title,
                html=html_content,
                js_api=self.api,
                width=1200,
                height=800,
                resizable=True,
                text_select=True
            )
        else:
            print(f"Loading HTML interface from: {html_path}")
            # Read the HTML file content and use it directly
            try:
                with open(html_path, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                print("HTML file loaded successfully")
                
                self.window = webview.create_window(
                    title=title,
                    html=html_content,
                    js_api=self.api,
                    width=1200,
                    height=800,
                    resizable=True,
                    text_select=True
                )
            except Exception as e:
                print(f"Error reading HTML file: {e}")
                # Fallback to simple HTML
                html_content = f"""
                <html>
                <body>
                    <h1>iflow - Project Artifact Manager</h1>
                    <p>Error reading interface file: {e}</p>
                </body>
                </html>
                """
                
                self.window = webview.create_window(
                    title=title,
                    html=html_content,
                    js_api=self.api,
                    width=1200,
                    height=800,
                    resizable=True,
                    text_select=True
                )
        
        # Start the webview
        webview.start(debug=True)
    
    def _create_api_proxy(self):
        """
        Create a completely isolated API that doesn't reference any complex objects.
        This approach uses a class with methods to ensure pywebview recognizes them as functions.
        """
        class APIProxy:
            def __init__(self, app_instance):
                self._app = app_instance
            
            def list_artifacts(self, artifact_type=None):
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
            
            def get_artifact(self, artifact_id):
                try:
                    artifact = self._app.db.get_artifact(artifact_id)
                    if artifact:
                        return self._app._artifact_to_dict(artifact)
                    return None
                except Exception as e:
                    print(f"Error getting artifact {artifact_id}: {e}")
                    return None
            
            def create_artifact(self, data):
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
            
            def update_artifact(self, artifact_id, data):
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
            
            def delete_artifact(self, artifact_id):
                try:
                    self._app.db.delete_artifact(artifact_id)
                    return True
                except Exception as e:
                    print(f"Error deleting artifact {artifact_id}: {e}")
                    return False
            
            def search_artifacts(self, query):
                try:
                    artifacts = self._app.db.search_artifacts(query)
                    return [self._app._artifact_to_dict(artifact) for artifact in artifacts]
                except Exception as e:
                    print(f"Error searching artifacts: {e}")
                    return []
            
            def get_stats(self):
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
        
        proxy = APIProxy(self)
        print(f"API proxy created with methods: {[method for method in dir(proxy) if not method.startswith('_')]}")
        return proxy
    
    def _artifact_to_dict(self, artifact: Artifact) -> Dict[str, Any]:
        """
        Convert an artifact to a dictionary for JSON serialization.
        
        Args:
            artifact: The artifact to convert
            
        Returns:
            Dictionary representation of the artifact
        """
        return {
            'artifact_id': artifact.artifact_id,
            'type': artifact.type.value,
            'summary': artifact.summary,
            'description': artifact.description,
            'created_at': artifact.created_at.isoformat(),
            'updated_at': artifact.updated_at.isoformat(),
            'metadata': artifact.metadata
        }
