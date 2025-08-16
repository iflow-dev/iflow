#!/usr/bin/env python3
"""
Simple demo script for iflow.
Run this from the root directory to see the package in action.
"""

import sys
import os
import argparse
import traceback

# Add the sw directory to the Python path to find the iflow package
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sw'))

try:
    from iflow import Artifact, ArtifactType, GitDatabase
    
    def main(debug=False):
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
        parser = argparse.ArgumentParser(description="iflow Demo Script")
        parser.add_argument("--debug", action="store_true", help="Enable debug mode with full stack traces")
        args = parser.parse_args()
        
        main(debug=args.debug)
        
except ImportError as e:
    print(f"Error importing iflow: {e}")
    print("Make sure you're running this from the root directory.")
    print("You can also install the package with: pip install -e .")
except Exception as e:
    print(f"Error running demo: {e}")
    if args.debug:
        print("\n" + "="*50)
        print("FULL STACK TRACE:")
        print("="*50)
        traceback.print_exc()
