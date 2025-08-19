#!/bin/bash

# Integration Environment Startup Script
# Purpose: Start the iflow integration environment for testing multiple PRs together
# Can be run from anywhere using: /opt/iflow/integration/start.sh

echo "Starting iflow Integration Environment..."

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Set environment variables
export IFLOW_ENVIRONMENT="integration"
export IFLOW_BASE_URL="http://localhost:8082"

# Change to the script directory
cd "$SCRIPT_DIR"

# Check if virtual environment exists, create if not
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install iflow package if not already installed
if ! pip show iflow > /dev/null 2>&1; then
    echo "Installing iflow package..."
    pip install /Users/claudio/realtime/reos2
fi

# Check if test database exists, clone if not
if [ ! -d ".iflow-test" ]; then
    echo "Setting up test database..."
    git clone https://github.com/iflow-dev/iflow-test-db.git .iflow-test
fi

# Start the web server
echo "Starting web server on port 8082..."
python -m iflow.web_server --port 8082 --database .iflow-test --host 0.0.0.0 --title "iflow - Integration Environment"
