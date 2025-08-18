# Integration Environment

## Purpose
The integration environment serves as a staging area for testing multiple pull requests together before merging them to the main branch.

## Key Features
- **Environment**: Dedicated environment for integration testing
- **Database**: Uses test-database from GitHub repository
- **Port**: 8082 (separate from dev:8080, qa:8081, prod:9000)
- **Purpose**: Test multiple PRs together to identify conflicts and integration issues

## Setup
1. Navigate to the integration environment directory:
   ```bash
   cd environments/integration
   ```

2. Start the integration environment:
   ```bash
   ./start_integration.sh
   ```

## What This Environment Does
- Creates a virtual environment for the iflow package
- Installs the iflow package from the development source
- Clones the test database from GitHub
- Starts the web server on port 8082
- Provides a clean environment for testing integrated changes

## Database
The integration environment uses the test database from the `iflow-test-db` GitHub repository, ensuring consistent test data across all environments.

## Access
Once started, the integration environment is accessible at:
- **URL**: http://localhost:8082
- **Title**: "iflow - Integration Environment"

## Notes
- This environment is focused on environment creation only
- Deployment process and advanced features will be implemented later
- The environment follows the same pattern as dev/qa/prod environments
