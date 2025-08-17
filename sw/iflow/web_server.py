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

# Global database instance - will be initialized when server starts
db = None

def create_app(database_path=".iflow"):
    """Create and configure the Flask app."""
    global db
    db = GitDatabase(database_path)
    return app

# Error handlers
@app.errorhandler(500)
def internal_error(error):
    """Handle 500 internal server errors."""
    print(f"500 Internal Server Error: {error}")
    import traceback
    traceback.print_exc()
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(Exception)
def handle_exception(e):
    """Handle any unhandled exceptions."""
    print(f"Unhandled exception: {e}")
    import traceback
    traceback.print_exc()
    return jsonify({'error': str(e)}), 500

# Routes
@app.route('/')
def index():
    """Serve the main HTML page."""
    return render_template_string(get_html_template())

@app.route('/api/stats')
def get_stats():
    """Get database statistics."""
    try:
        print("Getting database statistics...")
        stats = db.get_stats()
        print(f"Raw stats: {stats}")
        
        # Ensure datetime objects are serializable
        if 'last_commit' in stats and stats['last_commit']:
            commit_info = stats['last_commit']
            if hasattr(commit_info, 'get'):
                if 'date' in commit_info and hasattr(commit_info['date'], 'isoformat'):
                    commit_info['date'] = commit_info['date'].isoformat()
            elif hasattr(commit_info, 'isoformat'):
                stats['last_commit'] = commit_info.isoformat()
        
        print(f"Processed stats: {stats}")
        return jsonify(stats)
    except Exception as e:
        print(f"Error getting stats: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/artifacts')
def list_artifacts():
    """List all artifacts, optionally filtered by type."""
    try:
        artifact_type = request.args.get('type')
        print(f"Listing artifacts, type filter: {artifact_type}")
        
        if artifact_type:
            artifact_type_enum = ArtifactType(artifact_type)
            artifacts = db.list_artifacts(artifact_type_enum)
        else:
            artifacts = db.list_artifacts()
        
        print(f"Found {len(artifacts)} artifacts")
        
        # Convert to dictionaries for JSON serialization
        result = [artifact_to_dict(artifact) for artifact in artifacts]
        return jsonify(result)
    except Exception as e:
        print(f"Error listing artifacts: {e}")
        import traceback
        traceback.print_exc()
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
        print(f"Updating artifact: {artifact_id}")
        artifact = db.get_artifact(artifact_id)
        if not artifact:
            print(f"Artifact not found: {artifact_id}")
            return jsonify({'error': 'Artifact not found'}), 404
        
        data = request.get_json()
        print(f"Update data: {data}")
        
        # Update fields
        if 'type' in data:
            artifact.type = ArtifactType(data['type'])
        if 'summary' in data:
            artifact.summary = data['summary']
        if 'description' in data:
            artifact.description = data['description']
        
        # Update timestamp
        artifact.update()
        
        print(f"Artifact updated, saving to database...")
        # Save to database
        db.save_artifact(artifact)
        print(f"Artifact saved successfully")
        
        result = artifact_to_dict(artifact)
        print(f"Returning result: {result}")
        return jsonify(result)
    except Exception as e:
        print(f"Error updating artifact {artifact_id}: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/artifacts/<artifact_id>', methods=['DELETE'])
def delete_artifact(artifact_id):
    """Delete an artifact."""
    try:
        print(f"Attempting to delete artifact: {artifact_id}")
        db.delete_artifact(artifact_id)
        print(f"Successfully deleted artifact: {artifact_id}")
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error deleting artifact {artifact_id}: {e}")
        import traceback
        traceback.print_exc()
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
    global db
    # Initialize database with the correct path
    db = GitDatabase(database_path)
    
    print(f"Starting iflow web server...")
    print(f"Database: {database_path}")
    print(f"URL: http://{host}:{port}")
    print(f"Press Ctrl+C to stop")
    
    app.run(host=host, port=port, debug=debug)

# Note: This module is designed to be imported and used by run_web.py
# The run_web_server function should be called from the importing script
