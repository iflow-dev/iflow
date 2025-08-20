#!/usr/bin/env python3
"""
Simple script to start a local iflow web server.

Usage:
    python start_server.py [--port PORT] [--database PATH] [--init-db]
    
    Options:
        --port PORT        Port to run the server on (default: 8080)
        --database PATH    Path to the database to use for this instance
        --init-db          Initialize a new database
"""
import sys
import os
import argparse
import socket

# Add the sw/iflow directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sw'))

def is_port_free(port):
    """Check if a port is free to use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('localhost', port))
            return True
        except OSError:
            return False

def init_database(database_path):
    """Initialize a new iflow database with git repository and initial artifacts."""
    import subprocess
    import yaml
    from pathlib import Path
    
    db_path = Path(database_path)
    
    # Create database directory if it doesn't exist
    db_path.mkdir(parents=True, exist_ok=True)
    
    # Initialize git repository
    print(f"Initializing git repository in {db_path}")
    subprocess.run(['git', 'init'], cwd=db_path, check=True)
    
    # Create initial artifact 00001.yaml
    initial_artifact = {
        'artifact_id': '00001',
        'summary': 'Initial artifact',
        'description': 'This is the first artifact created when initializing the database.',
        'type': 'requirement',
        'status': 'open',
        'category': 'system',
        'created_at': '2025-08-20T00:00:00.000000',
        'updated_at': '2025-08-20T00:00:00.000000',
        'verification': 'NONE',
        'flagged': False,
        'metadata': {}
    }
    
    artifact_file = db_path / '00001.yaml'
    with open(artifact_file, 'w') as f:
        yaml.dump(initial_artifact, f, default_flow_style=False)
    
    print(f"Created initial artifact: {artifact_file}")
    
    # Add and commit the artifact
    subprocess.run(['git', 'add', '00001.yaml'], cwd=db_path, check=True)
    subprocess.run(['git', 'commit', '-m', 'Initial artifact: Initial artifact'], cwd=db_path, check=True)
    
    # Tag the initial version
    subprocess.run(['git', 'tag', 'v0.0.0'], cwd=db_path, check=True)
    
    print("Database initialization completed successfully!")
    print(f"Database location: {db_path.absolute()}")
    print("Initial artifact: 00001.yaml")
    print("Git tag: v0.0.0")

def main():
    parser = argparse.ArgumentParser(description='Start iflow web server')
    parser.add_argument('--port', type=int, default=8080, help='Port to run the server on (default: 8080)')
    parser.add_argument('--database', type=str, default='.iflow-demo', help='Path to the database to use for this instance')
    parser.add_argument('--init-db', action='store_true', help='Initialize a new database')
    
    args = parser.parse_args()
    
    # Check if port is free
    if not is_port_free(args.port):
        print(f"Error: Port {args.port} is already in use by another program.")
        print("Either identify and stop that program, or start the server with a different port.")
        sys.exit(1)
    
    try:
        from iflow.web_server import app
        print(f"Starting iflow web server on http://localhost:{args.port}")
        print(f"Using database: {args.database}")
        
        if args.init_db:
            print("Initializing new database...")
            init_database(args.database)
        
        # Use use_reloader=False to prevent the port check issue with Flask's auto-reloader
        app.run(host='0.0.0.0', port=args.port, debug=True, use_reloader=False)
    except ImportError as e:
        print(f"Import error: {e}")
        print("Make sure you're in the correct directory and dependencies are installed")
        sys.exit(1)
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
