"""
Main application module for iflow using pywebview.
"""

import webview
import json
import os
from typing import List, Dict, Any, Optional
from .core import Artifact, ArtifactType
from .database import GitDatabase
from .api import APIProxy


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
            # Read the HTML file content and inject CSS/JS directly
            try:
                with open(html_path, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                
                # Read CSS file
                css_path = os.path.join(os.path.dirname(__file__), 'static', 'styles.css')
                css_content = ""
                if os.path.exists(css_path):
                    with open(css_path, 'r', encoding='utf-8') as f:
                        css_content = f.read()
                    print("CSS file loaded successfully")
                else:
                    print("Warning: CSS file not found")
                
                # Read JavaScript file
                js_path = os.path.join(os.path.dirname(__file__), 'static', 'app.js')
                js_content = ""
                if os.path.exists(js_path):
                    with open(js_path, 'r', encoding='utf-8') as f:
                        js_content = f.read()
                    print("JavaScript file loaded successfully")
                else:
                    print("Warning: JavaScript file not found")
                
                # Inject CSS and JS into HTML
                html_content = html_content.replace('<link rel="stylesheet" href="styles.css">', f'<style>{css_content}</style>')
                html_content = html_content.replace('<script src="app.js"></script>', f'<script>{js_content}</script>')
                
                print("HTML interface prepared with embedded CSS and JavaScript")
                
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
                print(f"Error reading interface files: {e}")
                # Fallback to simple HTML
                html_content = f"""
                <html>
                <body>
                    <h1>iflow - Project Artifact Manager</h1>
                    <p>Error reading interface files: {e}</p>
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
        Create an API proxy instance for frontend communication.
        
        Returns:
            APIProxy instance with methods for artifact management
        """
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
