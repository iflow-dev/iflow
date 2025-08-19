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

### Run from anywhere
The startup script can be run from any directory:
```bash
/opt/iflow/integration/start.sh
```

### Manual startup
```bash
cd /opt/iflow/integration
source venv/bin/activate
python -m iflow.web_server --port 8082 --database .iflow-test --host 0.0.0.0 --title "iflow - Integration Environment"
```

## Environment Details
- **Working Directory**: `/opt/iflow/integration/`
- **Port**: 8082
- **Database**: `/opt/iflow/integration/.iflow-test`
- **Python Environment**: Dedicated virtual environment at `/opt/iflow/integration/venv/`
- **Code Source**: Installed iflow package
- **Purpose**: Integration testing of multiple pull requests
