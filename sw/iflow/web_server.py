"""
Flask web server for iflow application.

This module provides a web interface that can be accessed from any browser
instead of using pywebview.
"""

from flask import Flask, render_template_string, request, jsonify
from .core import Artifact, ArtifactType
from .database import GitDatabase
from .version import get_version_info

import os

# Create Flask app with static file serving
import os
# Get the absolute path to the static folder in the installed package
static_folder = os.path.join(os.path.dirname(__file__), 'static')
print(f"DEBUG: __file__ = {__file__}")
print(f"DEBUG: static_folder = {static_folder}")
print(f"DEBUG: static_folder exists = {os.path.exists(static_folder)}")
app = Flask(__name__, static_folder=static_folder, static_url_path='/static')

# Global variables
db = None
page_title = "iflow "

def init_database():
    """Initialize the database with the default path."""
    global db
    if db is None:
        # Check if environment variable is set
        env_db_path = os.environ.get("IFLOW_DATABASE_PATH")
        if env_db_path:
            print(f"Initializing database with environment path: {env_db_path}")
            db = GitDatabase(env_db_path)
        else:
            # Try to initialize with the default path
            default_db_path = "../../.iflow-demo"
            if os.path.exists(default_db_path):
                print(f"Initializing database with default path: {default_db_path}")
                db = GitDatabase(default_db_path)
            else:
                print(f"Default database path not found: {default_db_path}")
                # Fall back to the original default
                db = GitDatabase(".iflow")

# Initialize database when the module is imported
init_database()

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
    return render_template_string(get_html_template(page_title))

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

@app.route('/api/work-item-types')
def get_work_item_types():
    """Get available work item types from configuration."""
    try:
        work_item_types = db.config.get("work_item_types", [])
        return jsonify(work_item_types)
    except Exception as e:
        print(f"Error getting work item types: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/artifact-statuses')
def get_artifact_statuses():
    """Get available artifact statuses from configuration."""
    try:
        artifact_statuses = db.config.get("artifact_statuses", [])
        return jsonify(artifact_statuses)
    except Exception as e:
        print(f"Error getting artifact statuses: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/project-info')
def get_project_info():
    """Get project information from centralized version management."""
    try:
        # Get version from centralized version management
        version_info = get_version_info()
        
        # Get other project info from database config (excluding version)
        db_project_info = db.config.get("project", {})
        
        # Combine version info with database project info, prioritizing centralized version
        project_info = {
            "name": db_project_info.get("name", "iflow"),
            "description": db_project_info.get("description", "Git-based artifact management system"),
            "version": version_info["version"],
            "full_version": version_info["full_version"],
            "version_source": version_info["source"]
        }
        
        return jsonify(project_info)
    except Exception as e:
        print(f"Error getting project info: {e}")
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
            category=data.get('category', ''),
            status=data.get('status', 'open'),
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
        if 'category' in data:
            artifact.category = data['category']
        if 'status' in data:
            artifact.status = data['status']
        
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
        'category': artifact.category,
        'status': artifact.status,
        'created_at': artifact.created_at.isoformat(),
        'updated_at': artifact.updated_at.isoformat(),
        'metadata': artifact.metadata
    }

def get_html_template(title="iflow - Project Artifact Manager"):
    """Get the complete HTML template with embedded CSS and JS."""
    # Read the HTML file
    html_path = os.path.join(os.path.dirname(__file__), 'static', 'index.html')
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Update the title
    html_content = html_content.replace('<title>iflow - Project Artifact Manager</title>', f'<title>{title}</title>')
    
    # Also update the header
    html_content = html_content.replace('<h1>iflow - Project Artifact Manager</h1>', f'<h1>{title}</h1>')
    
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

def run_web_server(database_path=".iflow", host="127.0.0.1", port=5000, debug=True, init_db=False):
    """Run the Flask web server."""
    global db
    
    # Initialize database with initial artifact if requested
    if init_db:
        print("Initializing database with initial artifact...")
        try:
            # Create database instance
            init_db_instance = GitDatabase(database_path)
            
            # Create initial artifact
            from .core import Artifact, ArtifactType
            initial_artifact = Artifact(
                artifact_type=ArtifactType("requirement"),
                summary="Initial ticket",
                description="This is the initial ticket created when the database was initialized.",
                category="setup",
                status="open"
            )
            
            # Save the initial artifact
            init_db_instance.save_artifact(initial_artifact)
            print(f"✅ Created initial artifact: {initial_artifact.artifact_id} - {initial_artifact.summary}")
            
        except Exception as e:
            print(f"❌ Failed to initialize database: {e}")
            import traceback
            traceback.print_exc()
    
    # Initialize database with the correct path
    db = GitDatabase(database_path)
    
    print(f"Starting iflow web server...")
    print(f"Database: {database_path}")
    print(f"URL: http://{host}:{port}")
    print(f"Press Ctrl+C to stop")
    
    app.run(host=host, port=port, debug=debug)



# Note: This module is designed to be imported and used by run_web.py
# The run_web_server function should be called from the importing script

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="iflow Web Server")
    parser.add_argument("--port", type=int, default=5000, help="Port to run the server on")
    parser.add_argument("--database", type=str, default=".iflow-demo", help="Database path to use")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--title", type=str, default="iflow - Project Artifact Manager", help="Page title to display")
    parser.add_argument("--init-db", action="store_true", help="Initialize database with initial artifact")
    
    args = parser.parse_args()
    
    # Set the global title
    page_title = args.title
    
    print(f"Starting iflow web server...")
    print(f"Database: {args.database}")
    print(f"Host: {args.host}")
    print(f"Port: {args.port}")
    print(f"Title: {args.title}")
    print(f"Initialize DB: {args.init_db}")
    
    run_web_server(database_path=args.database, host=args.host, port=args.port, debug=False, init_db=args.init_db)
