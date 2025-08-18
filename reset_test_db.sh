#!/bin/bash

# Reset test database to base state
# This script resets the .iflow-test database to the 'base' tag
# which contains only one artifact (00001.yaml) for consistent testing

set -e

echo "Resetting test database to base state..."

# Navigate to test database directory
cd /opt/iflow/dev/.iflow-test

# Check if we're in the right directory
if [ ! -d ".git" ]; then
    echo "Error: Not in a git repository. Make sure you're in the .iflow-test directory."
    exit 1
fi

# Check if base tag exists
if ! git tag -l | grep -q "base"; then
    echo "Error: 'base' tag not found. Please create the base tag first."
    exit 1
fi

# Reset to base tag
echo "Resetting to base tag..."
git reset --hard base

# Clean any untracked files
echo "Cleaning untracked files..."
git clean -fd

# Verify the state
echo "Verifying database state..."
ARTIFACT_COUNT=$(ls artifacts/ | wc -l)
echo "Number of artifacts: $ARTIFACT_COUNT"

if [ "$ARTIFACT_COUNT" -eq 1 ]; then
    echo "✅ Database reset successful. Only artifact 00001.yaml remains."
else
    echo "❌ Database reset failed. Expected 1 artifact, found $ARTIFACT_COUNT"
    exit 1
fi

echo "Test database ready for testing!"
