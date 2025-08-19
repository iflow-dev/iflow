#!/usr/bin/env python3
"""
Script to sync test data across all environments and tag the database state.
This ensures all environments have the same test artifacts for consistent testing.
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
from iflow.database import GitDatabase


def sync_test_data():
    """Sync test data from .iflow-test to all environment databases."""
    
    # Source test database
    test_db_path = ".iflow-test"
    
    # Environment database paths
    env_paths = [
        "/opt/iflow/dev/database",
        "/opt/iflow/qa/database",
        "/opt/iflow/prod/database"
    ]
    
    print("🔄 Syncing test data across all environments...")
    
    # Verify source test database exists and has artifacts
    if not os.path.exists(test_db_path):
        print(f"❌ Test database not found: {test_db_path}")
        return False
    
    test_db = GitDatabase(test_db_path)
    test_artifacts = test_db.list_artifacts()
    
    if not test_artifacts:
        print(f"❌ No artifacts found in test database: {test_db_path}")
        return False
    
    print(f"✅ Found {len(test_artifacts)} artifacts in test database")
    for artifact in test_artifacts:
        print(f"   #{artifact.artifact_id} - {artifact.summary}")
    
    # Sync to each environment
    for env_path in env_paths:
        print(f"\n📁 Syncing to {env_path}...")
        
        # Create directory if it doesn't exist
        os.makedirs(env_path, exist_ok=True)
        
        # Remove existing artifacts directory
        artifacts_dir = os.path.join(env_path, "artifacts")
        if os.path.exists(artifacts_dir):
            shutil.rmtree(artifacts_dir)
        
        # Copy test database contents
        shutil.copytree(os.path.join(test_db_path, "artifacts"), artifacts_dir)
        
        # Copy git metadata if it exists
        git_dir = os.path.join(test_db_path, ".git")
        if os.path.exists(git_dir):
            env_git_dir = os.path.join(env_path, ".git")
            if os.path.exists(env_git_dir):
                shutil.rmtree(env_git_dir)
            shutil.copytree(git_dir, env_git_dir)
        
        # Verify sync
        try:
            env_db = GitDatabase(env_path)
            env_artifacts = env_db.list_artifacts()
            print(f"   ✅ Synced {len(env_artifacts)} artifacts")
        except Exception as e:
            print(f"   ❌ Error verifying {env_path}: {e}")
            return False
    
    print("\n✅ Test data sync completed successfully!")
    return True


def tag_database_state():
    """Tag the current database state in all environments."""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    tag_name = f"test-data-v1.0-{timestamp}"
    
    print(f"\n🏷️  Tagging database state: {tag_name}")
    
    # Tag test database
    test_db = GitDatabase(".iflow-test")
    try:
        test_db.repo.create_tag(tag_name, message=f"Test data state {timestamp}")
        print(f"   ✅ Tagged test database: {tag_name}")
    except Exception as e:
        print(f"   ⚠️  Could not tag test database: {e}")
    
    # Tag environment databases
    env_paths = [
        "/opt/iflow/dev/database",
        "/opt/iflow/qa/database",
        "/opt/iflow/prod/database"
    ]
    
    for env_path in env_paths:
        try:
            env_db = GitDatabase(env_path)
            env_db.repo.create_tag(tag_name, message=f"Test data state {timestamp}")
            print(f"   ✅ Tagged {env_path}: {tag_name}")
        except Exception as e:
            print(f"   ⚠️  Could not tag {env_path}: {e}")
    
    print(f"\n🏷️  Database state tagged as: {tag_name}")


def main():
    """Main function to sync test data and tag database state."""
    
    print("🚀 Starting test data synchronization...")
    
    # Sync test data
    if not sync_test_data():
        print("❌ Test data sync failed!")
        return 1
    
    # Tag database state
    tag_database_state()
    
    print("\n🎉 Test data synchronization and tagging completed!")
    return 0


if __name__ == "__main__":
    exit(main())
