#!/usr/bin/env python3
"""
Basic usage example for the iflow package.
"""

from iflow import Artifact, ArtifactType, GitDatabase, IFlowApp


def create_sample_artifacts():
    """Create sample artifacts to demonstrate the system."""
    
    # Initialize database
    db = GitDatabase(".iflow-demo")
    
    # Create a requirement
    requirement = Artifact(
        artifact_type=ArtifactType.REQUIREMENT,
        summary="User Authentication System",
        description="""
        Implement a secure user authentication system that includes:
        - User registration with email verification
        - Secure login with password hashing
        - Password reset functionality
        - Session management
        - Role-based access control
        """
    )
    
    # Create a task
    task = Artifact(
        artifact_type=ArtifactType.TASK,
        summary="Design Database Schema",
        description="Create the database schema for user management tables including users, roles, and permissions."
    )
    
    # Create a test case
    test_case = Artifact(
        artifact_type=ArtifactType.TEST_CASE,
        summary="Test User Registration Flow",
        description="""
        Test the complete user registration flow:
        1. User fills registration form
        2. Email verification is sent
        3. User clicks verification link
        4. Account is activated
        5. User can login
        """
    )
    
    # Create a bug
    bug = Artifact(
        artifact_type=ArtifactType.BUG,
        summary="Login Form Not Responsive on Mobile",
        description="The login form elements are too small and difficult to use on mobile devices."
    )
    
    # Save all artifacts
    artifacts = [requirement, task, test_case, bug]
    for artifact in artifacts:
        db.save_artifact(artifact)
        print(f"Created {artifact.type.value}: {artifact.summary}")
    
    return db


def demonstrate_database_operations(db):
    """Demonstrate various database operations."""
    
    print("\n" + "="*50)
    print("DATABASE OPERATIONS DEMONSTRATION")
    print("="*50)
    
    # List all artifacts
    print("\n1. All Artifacts:")
    all_artifacts = db.list_artifacts()
    for artifact in all_artifacts:
        print(f"  - {artifact.type.value}: {artifact.summary}")
    
    # Filter by type
    print("\n2. Requirements only:")
    requirements = db.list_artifacts(ArtifactType.REQUIREMENT)
    for req in requirements:
        print(f"  - {req.summary}")
    
    # Search artifacts
    print("\n3. Search for 'user':")
    user_artifacts = db.search_artifacts("user")
    for artifact in user_artifacts:
        print(f"  - {artifact.type.value}: {artifact.summary}")
    
    # Get statistics
    print("\n4. Database Statistics:")
    stats = db.get_stats()
    print(f"  Total artifacts: {stats['total_artifacts']}")
    print(f"  Total commits: {stats['total_commits']}")
    print(f"  By type: {stats['by_type']}")
    
    # Get artifact history
    if all_artifacts:
        first_artifact = all_artifacts[0]
        print(f"\n5. History for '{first_artifact.summary}':")
        history = db.get_artifact_history(first_artifact.artifact_id)
        for commit in history:
            print(f"  - {commit['date']}: {commit['message']}")


def run_web_interface():
    """Run the web-based interface."""
    
    print("\n" + "="*50)
    print("STARTING WEB INTERFACE")
    print("="*50)
    print("The web interface will open in a new window.")
    print("You can create, edit, and manage artifacts through the UI.")
    print("Press Ctrl+C to exit the application.")
    
    try:
        app = IFlowApp(database_path=".iflow-demo")
        app.run()
    except KeyboardInterrupt:
        print("\nExiting...")


def main():
    """Main demonstration function."""
    
    print("iflow - Project Artifact Manager")
    print("Basic Usage Example")
    print("="*50)
    
    # Create sample data
    print("Creating sample artifacts...")
    db = create_sample_artifacts()
    
    # Demonstrate operations
    demonstrate_database_operations(db)
    
    # Ask user if they want to run the web interface
    print("\n" + "="*50)
    response = input("Would you like to run the web interface? (y/n): ").lower().strip()
    
    if response in ['y', 'yes']:
        run_web_interface()
    else:
        print("Demo completed. You can run the web interface later with:")
        print("python -m iflow.main --database .iflow-demo")


if __name__ == "__main__":
    main()
