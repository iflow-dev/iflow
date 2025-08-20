#!/usr/bin/env python3
"""
Simple script to start a local iflow web server.

Usage:
    python start_server.py [--port PORT] [--init-db]
    
    Options:
        --port PORT    Port to run the server on (default: 8080)
        --init-db      Initialize a new database
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

# TODO: add --database for the path to the database to use for this instance
def main():
    parser = argparse.ArgumentParser(description='Start iflow web server')
    parser.add_argument('--port', type=int, default=8080, help='Port to run the server on (default: 8080)')
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
        
        if args.init_db:
            print("Initializing new database...")
            # TODO: Add database initialization logic here

                # TODO: init a new git repository in path `database`

                # TODO: create a new artifact 00001.yaml with summary "Initial artifact"

                # TODO: commit the new artifact

                # TODO: tag v0.0.0

        
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
