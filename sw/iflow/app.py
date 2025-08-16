"""
Main application module for iflow using pywebview.
"""

import webview
import json
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
        self.api = IFlowAPI(self.db)
    
    def run(self, title: str = "iflow - Project Artifact Manager"):
        """
        Run the iflow application.
        
        Args:
            title: Window title for the application
        """
        # Create the webview window
        self.window = webview.create_window(
            title=title,
            url='data:text/html,<html><body><h1>iflow</h1><p>Loading...</p></body></html>',
            js_api=self.api,
            width=1200,
            height=800,
            resizable=True,
            text_select=True
        )
        
        # Start the webview
        webview.start(debug=True)
    
    def get_html_interface(self) -> str:
        """
        Get the HTML interface for the application.
        
        Returns:
            HTML string containing the user interface
        """
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>iflow - Project Artifact Manager</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: #f5f5f5;
            color: #333;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1rem 2rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .header h1 {
            font-size: 2rem;
            font-weight: 300;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        .toolbar {
            background: white;
            padding: 1rem;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
            display: flex;
            gap: 1rem;
            align-items: center;
            flex-wrap: wrap;
        }
        
        .btn {
            background: #667eea;
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.9rem;
            transition: background 0.2s;
        }
        
        .btn:hover {
            background: #5a6fd8;
        }
        
        .btn-secondary {
            background: #6c757d;
        }
        
        .btn-secondary:hover {
            background: #5a6268;
        }
        
        .btn-danger {
            background: #dc3545;
        }
        
        .btn-danger:hover {
            background: #c82333;
        }
        
        .search-box {
            flex: 1;
            min-width: 200px;
            padding: 0.5rem;
            border: 1px solid #ddd;
            border-radius: 6px;
            font-size: 0.9rem;
        }
        
        .filter-select {
            padding: 0.5rem;
            border: 1px solid #ddd;
            border-radius: 6px;
            font-size: 0.9rem;
        }
        
        .artifacts-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
            gap: 1.5rem;
        }
        
        .artifact-card {
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .artifact-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        }
        
        .artifact-header {
            padding: 1rem;
            border-bottom: 1px solid #eee;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .artifact-type {
            background: #667eea;
            color: white;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 500;
            text-transform: uppercase;
        }
        
        .artifact-id {
            font-family: monospace;
            font-size: 0.8rem;
            color: #666;
        }
        
        .artifact-content {
            padding: 1rem;
        }
        
        .artifact-summary {
            font-size: 1.1rem;
            font-weight: 500;
            margin-bottom: 0.5rem;
            color: #333;
        }
        
        .artifact-description {
            color: #666;
            line-height: 1.5;
            margin-bottom: 1rem;
        }
        
        .artifact-meta {
            display: flex;
            justify-content: space-between;
            font-size: 0.8rem;
            color: #888;
        }
        
        .artifact-actions {
            padding: 1rem;
            border-top: 1px solid #eee;
            display: flex;
            gap: 0.5rem;
        }
        
        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.5);
        }
        
        .modal-content {
            background-color: white;
            margin: 5% auto;
            padding: 2rem;
            border-radius: 8px;
            width: 90%;
            max-width: 600px;
            max-height: 80vh;
            overflow-y: auto;
        }
        
        .form-group {
            margin-bottom: 1rem;
        }
        
        .form-label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 500;
        }
        
        .form-input, .form-textarea, .form-select {
            width: 100%;
            padding: 0.5rem;
            border: 1px solid #ddd;
            border-radius: 6px;
            font-size: 0.9rem;
        }
        
        .form-textarea {
            min-height: 100px;
            resize: vertical;
        }
        
        .stats-bar {
            background: white;
            padding: 1rem;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 1rem;
        }
        
        .stat-item {
            text-align: center;
        }
        
        .stat-number {
            font-size: 2rem;
            font-weight: bold;
            color: #667eea;
        }
        
        .stat-label {
            color: #666;
            font-size: 0.9rem;
        }
        
        .loading {
            text-align: center;
            padding: 2rem;
            color: #666;
        }
        
        .error {
            background: #f8d7da;
            color: #721c24;
            padding: 1rem;
            border-radius: 6px;
            margin-bottom: 1rem;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>iflow</h1>
        <p>Project Artifact Manager</p>
    </div>
    
    <div class="container">
        <div class="toolbar">
            <button class="btn" onclick="showCreateModal()">Create Artifact</button>
            <input type="text" class="search-box" placeholder="Search artifacts..." oninput="searchArtifacts(this.value)">
            <select class="filter-select" onchange="filterByType(this.value)">
                <option value="">All Types</option>
                <option value="requirement">Requirements</option>
                <option value="task">Tasks</option>
                <option value="test_case">Test Cases</option>
                <option value="issue">Issues</option>
                <option value="bug">Bugs</option>
                <option value="feature">Features</option>
                <option value="story">Stories</option>
            </select>
            <button class="btn btn-secondary" onclick="refreshArtifacts()">Refresh</button>
        </div>
        
        <div id="stats-bar" class="stats-bar">
            <div class="loading">Loading statistics...</div>
        </div>
        
        <div id="artifacts-container">
            <div class="loading">Loading artifacts...</div>
        </div>
    </div>
    
    <!-- Create/Edit Modal -->
    <div id="artifactModal" class="modal">
        <div class="modal-content">
            <h2 id="modalTitle">Create Artifact</h2>
            <form id="artifactForm">
                <div class="form-group">
                    <label class="form-label">Type</label>
                    <select class="form-select" id="artifactType" required>
                        <option value="requirement">Requirement</option>
                        <option value="task">Task</option>
                        <option value="test_case">Test Case</option>
                        <option value="issue">Issue</option>
                        <option value="bug">Bug</option>
                        <option value="feature">Feature</option>
                        <option value="story">Story</option>
                    </select>
                </div>
                <div class="form-group">
                    <label class="form-label">Summary</label>
                    <input type="text" class="form-input" id="artifactSummary" required>
                </div>
                <div class="form-group">
                    <label class="form-label">Description</label>
                    <textarea class="form-textarea" id="artifactDescription"></textarea>
                </div>
                <div class="form-group">
                    <label class="form-label">ID (leave empty for auto-generated)</label>
                    <input type="text" class="form-input" id="artifactId" placeholder="Auto-generated">
                </div>
                <div style="display: flex; gap: 1rem; justify-content: flex-end;">
                    <button type="button" class="btn btn-secondary" onclick="closeModal()">Cancel</button>
                    <button type="submit" class="btn">Save</button>
                </div>
            </form>
        </div>
    </div>
    
    <script>
        let currentArtifacts = [];
        let editingArtifactId = null;
        
        // Initialize the application
        document.addEventListener('DOMContentLoaded', function() {
            loadStats();
            loadArtifacts();
        });
        
        // Load database statistics
        async function loadStats() {
            try {
                const stats = await pywebview.api.get_stats();
                displayStats(stats);
            } catch (error) {
                console.error('Error loading stats:', error);
                document.getElementById('stats-bar').innerHTML = '<div class="error">Error loading statistics</div>';
            }
        }
        
        // Display statistics
        function displayStats(stats) {
            const statsBar = document.getElementById('stats-bar');
            statsBar.innerHTML = `
                <div class="stat-item">
                    <div class="stat-number">${stats.total_artifacts}</div>
                    <div class="stat-label">Total Artifacts</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">${stats.total_commits}</div>
                    <div class="stat-label">Total Commits</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">${Object.keys(stats.by_type).length}</div>
                    <div class="stat-label">Artifact Types</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">${stats.last_commit ? '✓' : '✗'}</div>
                    <div class="stat-label">Git Status</div>
                </div>
            `;
        }
        
        // Load all artifacts
        async function loadArtifacts() {
            try {
                const artifacts = await pywebview.api.list_artifacts();
                currentArtifacts = artifacts;
                displayArtifacts(artifacts);
            } catch (error) {
                console.error('Error loading artifacts:', error);
                document.getElementById('artifacts-container').innerHTML = '<div class="error">Error loading artifacts</div>';
            }
        }
        
        // Display artifacts in the grid
        function displayArtifacts(artifacts) {
            const container = document.getElementById('artifacts-container');
            
            if (artifacts.length === 0) {
                container.innerHTML = '<div class="loading">No artifacts found. Create your first artifact to get started!</div>';
                return;
            }
            
            container.innerHTML = artifacts.map(artifact => `
                <div class="artifact-card">
                    <div class="artifact-header">
                        <span class="artifact-type">${artifact.type}</span>
                        <span class="artifact-id">${artifact.artifact_id}</span>
                    </div>
                    <div class="artifact-content">
                        <div class="artifact-summary">${artifact.summary}</div>
                        <div class="artifact-description">${artifact.description || 'No description'}</div>
                        <div class="artifact-meta">
                            <span>Created: ${new Date(artifact.created_at).toLocaleDateString()}</span>
                            <span>Updated: ${new Date(artifact.updated_at).toLocaleDateString()}</span>
                        </div>
                    </div>
                    <div class="artifact-actions">
                        <button class="btn btn-secondary" onclick="editArtifact('${artifact.artifact_id}')">Edit</button>
                        <button class="btn btn-danger" onclick="deleteArtifact('${artifact.artifact_id}')">Delete</button>
                    </div>
                </div>
            `).join('');
        }
        
        // Search artifacts
        async function searchArtifacts(query) {
            if (query.trim() === '') {
                displayArtifacts(currentArtifacts);
                return;
            }
            
            try {
                const results = await pywebview.api.search_artifacts(query);
                displayArtifacts(results);
            } catch (error) {
                console.error('Error searching artifacts:', error);
            }
        }
        
        // Filter artifacts by type
        async function filterByType(type) {
            if (type === '') {
                displayArtifacts(currentArtifacts);
                return;
            }
            
            try {
                const filtered = await pywebview.api.list_artifacts(type);
                displayArtifacts(filtered);
            } catch (error) {
                console.error('Error filtering artifacts:', error);
            }
        }
        
        // Show create artifact modal
        function showCreateModal() {
            editingArtifactId = null;
            document.getElementById('modalTitle').textContent = 'Create Artifact';
            document.getElementById('artifactForm').reset();
            document.getElementById('artifactId').value = '';
            document.getElementById('artifactModal').style.display = 'block';
        }
        
        // Show edit artifact modal
        async function editArtifact(artifactId) {
            try {
                const artifact = await pywebview.api.get_artifact(artifactId);
                if (artifact) {
                    editingArtifactId = artifactId;
                    document.getElementById('modalTitle').textContent = 'Edit Artifact';
                    document.getElementById('artifactType').value = artifact.type;
                    document.getElementById('artifactSummary').value = artifact.summary;
                    document.getElementById('artifactDescription').value = artifact.description || '';
                    document.getElementById('artifactId').value = artifact.artifact_id;
                    document.getElementById('artifactModal').style.display = 'block';
                }
            } catch (error) {
                console.error('Error loading artifact for editing:', error);
            }
        }
        
        // Close modal
        function closeModal() {
            document.getElementById('artifactModal').style.display = 'none';
        }
        
        // Handle form submission
        document.getElementById('artifactForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = {
                type: document.getElementById('artifactType').value,
                summary: document.getElementById('artifactSummary').value,
                description: document.getElementById('artifactDescription').value,
                artifact_id: document.getElementById('artifactId').value || null
            };
            
            try {
                if (editingArtifactId) {
                    await pywebview.api.update_artifact(editingArtifactId, formData);
                } else {
                    await pywebview.api.create_artifact(formData);
                }
                
                closeModal();
                loadStats();
                loadArtifacts();
            } catch (error) {
                console.error('Error saving artifact:', error);
                alert('Error saving artifact: ' + error.message);
            }
        });
        
        // Delete artifact
        async function deleteArtifact(artifactId) {
            if (confirm('Are you sure you want to delete this artifact?')) {
                try {
                    await pywebview.api.delete_artifact(artifactId);
                    loadStats();
                    loadArtifacts();
                } catch (error) {
                    console.error('Error deleting artifact:', error);
                    alert('Error deleting artifact: ' + error.message);
                }
            }
        }
        
        // Refresh artifacts
        function refreshArtifacts() {
            loadStats();
            loadArtifacts();
        }
        
        // Close modal when clicking outside
        window.onclick = function(event) {
            const modal = document.getElementById('artifactModal');
            if (event.target === modal) {
                closeModal();
            }
        }
    </script>
</body>
</html>
        """
    
    def create_webview_interface(self):
        """Create and return the webview interface HTML."""
        html_content = self.get_html_interface()
        
        # Create a temporary HTML file
        import tempfile
        import os
        
        temp_dir = tempfile.mkdtemp()
        html_file = os.path.join(temp_dir, 'iflow.html')
        
        with open(html_file, 'w') as f:
            f.write(html_content)
        
        return html_file


class IFlowAPI:
    """
    API class for communication between the frontend and backend.
    
    This class exposes methods that can be called from the JavaScript frontend
    to interact with the artifact database.
    """
    
    def __init__(self, database: GitDatabase):
        """
        Initialize the API with a database instance.
        
        Args:
            database: The git database instance
        """
        self.db = database
    
    def list_artifacts(self, artifact_type: str = None) -> List[Dict[str, Any]]:
        """
        List all artifacts, optionally filtered by type.
        
        Args:
            artifact_type: Optional artifact type filter
            
        Returns:
            List of artifacts as dictionaries
        """
        try:
            if artifact_type:
                artifact_type_enum = ArtifactType(artifact_type)
                artifacts = self.db.list_artifacts(artifact_type_enum)
            else:
                artifacts = self.db.list_artifacts()
            
            # Convert to dictionaries for JSON serialization
            return [self._artifact_to_dict(artifact) for artifact in artifacts]
        except Exception as e:
            print(f"Error listing artifacts: {e}")
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
            artifact = self.db.get_artifact(artifact_id)
            if artifact:
                return self._artifact_to_dict(artifact)
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
            
            self.db.save_artifact(artifact)
            return self._artifact_to_dict(artifact)
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
            artifact = self.db.get_artifact(artifact_id)
            if not artifact:
                raise ValueError(f"Artifact {artifact_id} not found")
            
            # Update the artifact
            if 'type' in data:
                artifact.type = ArtifactType(data['type'])
            if 'summary' in data:
                artifact.summary = data['summary']
            if 'description' in data:
                artifact.description = data['description']
            
            self.db.update_artifact(artifact)
            return self._artifact_to_dict(artifact)
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
            self.db.delete_artifact(artifact_id)
            return True
        except Exception as e:
            print(f"Error deleting artifact {artifact_id}: {e}")
            raise e
    
    def search_artifacts(self, query: str) -> List[Dict[str, Any]]:
        """
        Search artifacts by text.
        
        Args:
            query: Search query string
            
        Returns:
            List of matching artifacts as dictionaries
        """
        try:
            artifacts = self.db.search_artifacts(query)
            return [self._artifact_to_dict(artifact) for artifact in artifacts]
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
            return self.db.get_stats()
        except Exception as e:
            print(f"Error getting stats: {e}")
            return {
                'total_artifacts': 0,
                'by_type': {},
                'total_commits': 0,
                'last_commit': None
            }
    
    def _artifact_to_dict(self, artifact: Artifact) -> Dict[str, Any]:
        """
        Convert an Artifact object to a dictionary for JSON serialization.
        
        Args:
            artifact: The artifact object
            
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
