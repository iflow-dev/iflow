# Environment Setup

This document describes the setup and details of all environments used in the iflow project.

## Environments Overview

All environments follow the standard pattern `/opt/iflow/<env>/start.sh` and can be started from anywhere without changing directories.

### Development Environment
- **Working Directory**: `/opt/iflow/dev/`
- **Port**: 8080
- **Database**: `/opt/iflow/dev/.iflow-test`
- **Start Command**: `/opt/iflow/dev/start.sh`
- **Server Management**: `/opt/iflow/dev/server {start|stop|status|restart}`
- **Purpose**: Local development and testing

### QA Environment
- **Working Directory**: `/opt/iflow/qa/`
- **Port**: 8081
- **Database**: `/opt/iflow/qa/.iflow-test`
- **Start Command**: `/opt/iflow/qa/start.sh`
- **Server Management**: `/opt/iflow/qa/server {start|stop|status|restart}`
- **Purpose**: Quality assurance testing

### Production Environment
- **Working Directory**: `/opt/iflow/prod/`
- **Port**: 9000
- **Database**: `/opt/iflow/prod/.iflow-demo`
- **Start Command**: `/opt/iflow/prod/start.sh`
- **Server Management**: `/opt/iflow/prod/server {start|stop|status|restart}`
- **Purpose**: Production deployment

### Integration Environment
- **Working Directory**: `/opt/iflow/integration/`
- **Port**: 8082
- **Database**: `/opt/iflow/integration/.iflow-test`
- **Start Command**: `/opt/iflow/integration/start.sh`
- **Server Management**: `/opt/iflow/integration/server {start|stop|status|restart}`
- **Purpose**: Integration testing of multiple PRs

## Key Features

- **Universal Access**: All start scripts can be run from anywhere using `/opt/iflow/<env>/start.sh`
- **Unified Server Management**: All environments support `/opt/iflow/<env>/server` commands
- **Automatic Setup**: Scripts automatically handle virtual environment creation, package installation, and database setup
- **Consistent Pattern**: All environments follow the same startup pattern and structure
- **Port Management**: Each environment uses a unique port to avoid conflicts
- **Database Isolation**: Each environment has its own isolated database
- **Background Execution**: All servers start in background with proper PID management

## Usage Examples

### Traditional Startup (Legacy)
```bash
# Start development environment from anywhere
/opt/iflow/dev/start.sh

# Start QA environment from anywhere
/opt/iflow/qa/start.sh

# Start production environment from anywhere
/opt/iflow/prod/start.sh

# Start integration environment from anywhere
/opt/iflow/integration/start.sh
```

### Unified Server Management (Recommended)
```bash
# Check status of all environments
/opt/iflow/dev/server status
/opt/iflow/qa/server status
/opt/iflow/prod/server status
/opt/iflow/integration/server status

# Start environments
/opt/iflow/dev/server start
/opt/iflow/qa/server start
/opt/iflow/prod/server start
/opt/iflow/integration/server start

# Stop environments
/opt/iflow/dev/server stop
/opt/iflow/qa/server stop
/opt/iflow/prod/server stop
/opt/iflow/integration/server stop

# Restart environments
/opt/iflow/dev/server restart
/opt/iflow/qa/server restart
/opt/iflow/prod/server restart
/opt/iflow/integration/server restart
```

## Server Management Features

### Start Command
- **Fails if server is already running** (prevents duplicate instances)
- Automatically handles all setup requirements
- Starts server in background with PID tracking
- Provides immediate feedback on success/failure

### Stop Command
- Gracefully shuts down server
- Waits for clean termination (up to 10 seconds)
- Force kills if necessary
- Cleans up PID files

### Status Command
- Shows current server status
- Displays PID and port information
- Color-coded output for clarity
- Validates port is actually listening

### Restart Command
- Stops existing server (if running)
- Starts new server instance
- Useful for applying configuration changes

## Configuration

All environments use the same `config.yaml` file for consistency. Environment-specific settings are handled through environment variables and startup scripts.

## File Locations

- **Startup Scripts**: `/opt/iflow/<env>/start.sh` (legacy, still supported)
- **Server Management**: `/opt/iflow/<env>/server` (recommended)
- **Repository Scripts**: `environments/server-scripts/` (for version control)
- **Documentation**: `environments/server-scripts/README.md`


