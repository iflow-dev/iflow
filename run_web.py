#!/usr/bin/env python3
"""
Simple script to run the iflow web server.
"""

import sys
import os

# Add the sw directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'sw'))

from iflow.web_server import run_web_server

if __name__ == "__main__":
    # Get database path from command line argument or use default
    database_path = sys.argv[1] if len(sys.argv) > 1 else ".iflow-demo"
    
    print(f"Starting iflow web server...")
    print(f"Database: {database_path}")
    print(f"URL: http://127.0.0.1:5000")
    print(f"Press Ctrl+C to stop")
    
    try:
        run_web_server(database_path, host="127.0.0.1", port=8080, debug=True)
    except KeyboardInterrupt:
        print("\nShutting down server...")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
