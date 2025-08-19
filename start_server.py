#!/usr/bin/env python3
"""
Simple script to start the iflow web server.
"""
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from sw.iflow.web_server import app
    print("Starting iflow web server on http://localhost:8080")
    app.run(host='0.0.0.0', port=8080, debug=True)
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure you're in the correct directory and dependencies are installed")
    sys.exit(1)
except Exception as e:
    print(f"Error starting server: {e}")
    sys.exit(1)
