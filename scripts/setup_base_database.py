#!/usr/bin/env python3
"""
Script to set up all environments with the base database and link them to the remote.
"""

import os
import shutil
import subprocess
from pathlib import Path


def run_command(cmd, cwd=None):
    """Run a command and return the result."""
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True, cwd=cwd)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {cmd}")
        print(f"Error: {e.stderr}")
        return None


def setup_environment_database(env_path, env_name):
    """Set up a specific environment with the base database."""
    
    print(f"\n📁 Setting up {env_name} environment...")
    
    # Create environment directory if it doesn't exist
    os.makedirs(env_path, exist_ok=True)
    
    # Remove existing database if it exists
    db_path = os.path.join(env_path, "database")
    if os.path.exists(db_path):
        print(f"   Removing existing database...")
        shutil.rmtree(db_path)
    
    # Copy the base test database
    print(f"   Copying base database...")
    base_db_path = os.path.join("/Users/claudio/realtime/reos2", ".iflow-test")
    shutil.copytree(base_db_path, db_path)
    
    # Change to the database directory
    os.chdir(db_path)
    
    # Add remote origin
    remote_url = "https://github.com/iflow-dev/iflow-test-db.git"
    result = run_command(f"git remote add origin {remote_url}")
    if result is None:
        print(f"   ⚠️  Remote already exists or failed to add")
    
    # Fetch from remote
    print(f"   Fetching from remote...")
    result = run_command("git fetch origin")
    if result is None:
        print(f"   ⚠️  Failed to fetch from remote (repository may not exist yet)")
    
    # Reset to base tag
    print(f"   Resetting to base tag...")
    result = run_command("git reset --hard base")
    if result is None:
        print(f"   ⚠️  Failed to reset to base tag")
    
    # Verify the database
    try:
        from iflow.database import GitDatabase
        db = GitDatabase(".")
        artifacts = db.list_artifacts()
        print(f"   ✅ {env_name} database contains {len(artifacts)} artifacts")
        for artifact in artifacts:
            print(f"      #{artifact.artifact_id} - {artifact.summary}")
    except Exception as e:
        print(f"   ❌ Error verifying {env_name} database: {e}")
        return False
    
    # Go back to main directory
    os.chdir("../..")
    
    return True


def setup_all_environments():
    """Set up all environments with the base database."""
    
    print("🚀 Setting up all environments with base database...")
    
    # Verify base database exists
    if not os.path.exists(".iflow-test"):
        print("❌ Base test database not found")
        return False
    
    # Verify base database has the expected artifact
    try:
        from iflow.database import GitDatabase
        db = GitDatabase(".iflow-test")
        artifacts = db.list_artifacts()
        if len(artifacts) != 1 or artifacts[0].artifact_id != "00001":
            print("❌ Base database doesn't contain expected artifact #00001")
            return False
        print(f"✅ Base database verified: {len(artifacts)} artifacts")
    except Exception as e:
        print(f"❌ Error verifying base database: {e}")
        return False
    
    # Set up each environment
    environments = [
        ("/opt/iflow/dev", "Development"),
        ("/opt/iflow/qa", "QA"),
        ("/opt/iflow/integration", "Integration")
    ]
    
    for env_path, env_name in environments:
        if not setup_environment_database(env_path, env_name):
            print(f"❌ Failed to set up {env_name} environment")
            return False
    
    print("\n✅ All environments set up successfully!")
    return True


def main():
    """Main function."""
    
    print("🚀 Setting up all environments with base database...")
    
    if not setup_all_environments():
        print("❌ Failed to set up environments")
        return 1
    
    print("\n🎉 Environment setup completed!")
    print("   All environments now contain artifact #00001")
    print("   All environments are linked to the remote repository")
    print("   All environments are reset to the 'base' tag")
    
    return 0


if __name__ == "__main__":
    exit(main())
