"""
Flask web server for iflow application.

This module provides a web interface that can be accessed from any browser
instead of using pywebview.
"""

from flask import Flask, render_template_string, request, jsonify
from .core import Artifact, ArtifactType
from .database import GitDatabase
import os

# Create Flask app
app = Flask(__name__)

# Global database instance
db = None

def create_app(database_path=".iflow"):
    """Create and configure the Flask app."""
    global db
    db = GitDatabase(database_path)
    
    # Register routes
    register_routes()
    
    return app

def register_routes():
    """Register all the Flask routes."""
    
    @app.route('/')
    def index():
        """Serve the main HTML page."""
        return render_template_string(get_html_template())
    
    @app.route('/api/stats')
    def get_stats():
        """Get database statistics."""
        try:
            stats = db.get_stats()
            # Ensure datetime objects are serializable
            if 'last_commit' in stats and stats['last_commit']:
                commit_info = stats['last_commit']
                if hasattr(commit_info, 'get'):
                    if 'date' in commit_info and hasattr(commit_info['date'], 'isoformat'):
                        commit_info['date'] = commit_info['date'].isoformat()
                elif hasattr(commit_info, 'isoformat'):
                    stats['last_commit'] = commit_info.isoformat()
            return jsonify(stats)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/artifacts')
    def list_artifacts():
        """List all artifacts, optionally filtered by type."""
        try:
            artifact_type = request.args.get('type')
            if artifact_type:
                artifact_type_enum = ArtifactType(artifact_type)
                artifacts = db.list_artifacts(artifact_type_enum)
            else:
                artifacts = db.list_artifacts()
            
            # Convert to dictionaries for JSON serialization
            result = [artifact_to_dict(artifact) for artifact in artifacts]
            return jsonify(result)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/artifacts/<artifact_id>')
    def get_artifact(artifact_id):
        """Get a specific artifact by ID."""
        try:
            artifact = db.get_artifact(artifact_id)
            if artifact:
                return jsonify(artifact_to_dict(artifact))
            return jsonify({'error': 'Artifact not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/artifacts', methods=['POST'])
    def create_artifact():
        """Create a new artifact."""
        try:
            data = request.get_json()
            artifact = Artifact(
                artifact_type=ArtifactType(data['type']),
                summary=data['summary'],
                description=data.get('description', ''),
                artifact_id=data.get('artifact_id')
            )
            
            db.save_artifact(artifact)
            return jsonify(artifact_to_dict(artifact)), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/artifacts/<artifact_id>', methods=['PUT'])
    def update_artifact(artifact_id):
        """Update an existing artifact."""
        try:
            artifact = db.get_artifact(artifact_id)
            if not artifact:
                return jsonify({'error': 'Artifact not found'}), 404
            
            data = request.get_json()
            
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
            db.save_artifact(artifact)
            return jsonify(artifact_to_dict(artifact))
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/artifacts/<artifact_id>', methods=['DELETE'])
    def delete_artifact(artifact_id):
        """Delete an artifact."""
        try:
            db.delete_artifact(artifact_id)
            return jsonify({'success': True})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/search')
    def search_artifacts():
        """Search artifacts by text."""
        try:
            query = request.args.get('q', '')
            if not query:
                return jsonify([])
            
            artifacts = db.search_artifacts(query)
            result = [artifact_to_dict(artifact) for artifact in artifacts]
            return jsonify(result)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

def artifact_to_dict(artifact):
    """Convert an artifact to a dictionary for JSON serialization."""
    return {
        'artifact_id': artifact.artifact_id,
        'type': artifact.type.value,
        'summary': artifact.summary,
        'description': artifact.description,
        'created_at': artifact.created_at.isoformat(),
        'updated_at': artifact.updated_at.isoformat(),
        'metadata': artifact.metadata
    }

def get_html_template():
    """Get the complete HTML template with embedded CSS and JS."""
    # Read the HTML file
    html_path = os.path.join(os.path.dirname(__file__), 'static', 'index.html')
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Read CSS file
    css_path = os.path.join(os.path.dirname(__file__), 'static', 'styles.css')
    css_content = ""
    if os.path.exists(css_path):
        with open(css_path, 'r', encoding='utf-8') as f:
            css_content = f.read()
    
    # Read JavaScript file (web version)
    js_path = os.path.join(os.path.dirname(__file__), 'static', 'app_web.js')
    js_content = ""
    if os.path.exists(js_path):
        with open(js_path, 'r', encoding='utf-8') as f:
            js_content = f.read()
    
    # Inject CSS and JS into HTML
    html_content = html_content.replace('<link rel="stylesheet" href="styles.css">', f'<style>{css_content}</style>')
    html_content = html_content.replace('<script src="app.js"></script>', f'<script>{js_content}</script>')
    
    return html_content

def run_web_server(database_path=".iflow", host="127.0.0.1", port=5000, debug=True):
    """Run the Flask web server."""
    app_instance = create_app(database_path)
    
    print(f"Starting iflow web server...")
    print(f"Database: {database_path}")
    print(f"URL: http://{host}:{port}")
    print(f"Press Ctrl+C to stop")
    
    app_instance.run(host=host, port=port, debug=debug)

if __name__ == "__main__":
    import sys
    database_path = sys.argv[1] if len(sys.argv) > 1 else ".iflow"
    run_web_server(database_path)
