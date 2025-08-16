#!/usr/bin/env python3
"""
Simple demo script for iflow.
Run this to see the package in action.
"""

import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from iflow import Artifact, ArtifactType, GitDatabase
    
    def main():
        print("iflow Demo")
        print("=" * 40)
        
        # Create a database
        db = GitDatabase(".iflow-demo")
        
        # Create some sample artifacts
        print("Creating sample artifacts...")
        
        req = Artifact(
            artifact_type=ArtifactType.REQUIREMENT,
            summary="User Login System",
            description="Implement secure user authentication"
        )
        
        task = Artifact(
            artifact_type=ArtifactType.TASK,
            summary="Design Database Schema",
            description="Create tables for users and sessions"
        )
        
        # Save artifacts
        db.save_artifact(req)
        db.save_artifact(task)
        
        print(f"✓ Created requirement: {req.summary}")
        print(f"✓ Created task: {task.summary}")
        
        # List all artifacts
        print("\nAll artifacts:")
        artifacts = db.list_artifacts()
        for artifact in artifacts:
            print(f"  - {artifact.type.value}: {artifact.summary}")
        
        # Get statistics
        stats = db.get_stats()
        print(f"\nDatabase stats: {stats['total_artifacts']} artifacts, {stats['total_commits']} commits")
        
        print("\nDemo completed! Run 'python -m iflow.main --database .iflow-demo' to start the web interface.")
        
    if __name__ == "__main__":
        main()
        
except ImportError as e:
    print(f"Error importing iflow: {e}")
    print("Make sure you're running this from the correct directory.")
    print("You can also install the package with: pip install -e .")
except Exception as e:
    print(f"Error running demo: {e}")
