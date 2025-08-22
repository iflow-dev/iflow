"""
Step definitions for database verification tests.
"""

from radish import step, world
from selenium.webdriver.common.by import By
from controls.artifact_control import Artifacts
import subprocess
import os
import tempfile


@step("I check the database state")
def i_check_database_state(step):
    """Check the current state of the database."""
    # This step is mainly for documentation - the actual verification happens in the "Then" steps
    pass


# Use existing step: "I see {count:d} search results" from artifact_creation_steps.py

@step("the artifact should have {property} {value:QuotedString}")
def the_artifact_should_have_property(step, property, value):
    """Generic step to verify that an artifact has a specific property value."""
    # Find artifacts and check if any have the specified property value
    artifacts = Artifacts().wait().find()
    
    # Look for the artifact with the specified property value in the text content
    found = False
    for artifact_element in artifacts:
        element_text = artifact_element.text
        if value in element_text:
            found = True
            break
    
    assert found, f"Artifact with {property} '{value}' not found in the database"


# Use the generic property verification step: "the artifact should have {property} {value:QuotedString}"


# Use existing step: "the artifact {should|should not} be flagged" from artifact_flags_steps.py


@step("I check the database repository")
def i_check_database_repository(step):
    """Check the database repository state."""
    # This step is mainly for documentation - the actual verification happens in the "Then" steps
    pass


@step("the repository should have tag {tag:QuotedString}")
def the_repository_should_have_tag(step, tag):
    """Verify that the repository has the specified tag."""
    # Get the database path from environment or use default
    db_path = os.environ.get('IFLOW_DATABASE_PATH', '.iflow-local')
    
    # Check if the tag exists in the git repository
    try:
        result = subprocess.run(
            ['git', 'tag', '--list', tag],
            cwd=db_path,
            capture_output=True,
            text=True,
            check=True
        )
        
        tags = result.stdout.strip().split('\n')
        assert tag in tags, f"Tag '{tag}' not found in repository. Available tags: {tags}"
        
    except subprocess.CalledProcessError as e:
        raise AssertionError(f"Failed to check git tags: {e}")


@step("the repository should have exactly {count:d} commit")
def the_repository_should_have_exactly_count_commits(step, count):
    """Verify that the repository has exactly the specified number of commits."""
    # Get the database path from environment or use default
    db_path = os.environ.get('IFLOW_DATABASE_PATH', '.iflow-local')
    
    # Count the commits in the repository
    try:
        result = subprocess.run(
            ['git', 'rev-list', '--count', 'HEAD'],
            cwd=db_path,
            capture_output=True,
            text=True,
            check=True
        )
        
        actual_count = int(result.stdout.strip())
        assert actual_count == count, f"Expected {count} commit(s), but found {actual_count}"
        
    except subprocess.CalledProcessError as e:
        raise AssertionError(f"Failed to count git commits: {e}")
    except ValueError as e:
        raise AssertionError(f"Failed to parse commit count: {e}")
