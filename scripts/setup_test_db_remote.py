#!/usr/bin/env python3
"""
Script to set up the remote repository for the test database and push to GitHub.
"""

import os
import subprocess
import sys
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


def setup_test_db_remote():
    """Set up the remote repository for the test database."""
    
    test_db_path = ".iflow-test"
    
    if not os.path.exists(test_db_path):
        print(f"❌ Test database not found: {test_db_path}")
        return False
    
    print("🔄 Setting up remote repository for test database...")
    
    # Change to test database directory
    os.chdir(test_db_path)
    
    # Check if remote already exists
    remote_url = run_command("git remote get-url origin")
    
    if remote_url:
        print(f"✅ Remote already configured: {remote_url}")
    else:
        # Create a new GitHub repository (this would require GitHub CLI or manual creation)
        print("📝 Please create a new GitHub repository for the test database.")
        print("   You can do this manually at: https://github.com/new")
        print("   Repository name: iflow-test-db")
        print("   Make it public")
        print("   Don't initialize with README, .gitignore, or license")
        
        # Wait for user to create the repository
        input("Press Enter after creating the repository...")
        
        # Add the remote
        remote_url = "https://github.com/iflow-dev/iflow-test-db.git"
        result = run_command(f"git remote add origin {remote_url}")
        
        if result is None:
            print("❌ Failed to add remote")
            return False
        
        print(f"✅ Added remote: {remote_url}")
    
    # Push to GitHub
    print("📤 Pushing to GitHub...")
    
    # Push the master branch
    result = run_command("git push -u origin master")
    if result is None:
        print("❌ Failed to push master branch")
        return False
    
    # Push the base tag
    result = run_command("git push origin base")
    if result is None:
        print("❌ Failed to push base tag")
        return False
    
    print("✅ Successfully pushed to GitHub")
    
    # Go back to main directory
    os.chdir("..")
    
    return True


def main():
    """Main function."""
    
    print("🚀 Setting up test database remote repository...")
    
    if not setup_test_db_remote():
        print("❌ Failed to set up remote repository")
        return 1
    
    print("\n🎉 Test database remote setup completed!")
    print("   Repository: https://github.com/iflow-dev/iflow-test-db")
    print("   Base tag: base")
    
    return 0


if __name__ == "__main__":
    exit(main())
