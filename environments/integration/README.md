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
   ./start.sh
   ```

## Alternative Startup Methods
The integration environment can also be started from anywhere using the standard pattern:

```bash
# From anywhere in the system
/opt/iflow/integration/start.sh
```

## Requirements
All required dependencies are automatically installed:
- Python 3.x
- Virtual environment (created automatically)
- iflow package (installed from source)
- Test database (cloned from GitHub)

## Script Pattern
This environment follows the standard `/opt/iflow/<env>/start.sh` pattern:
- Script can be run from anywhere
- Uses absolute paths for reliability
- Automatically changes to the correct directory
- Handles all setup automatically
