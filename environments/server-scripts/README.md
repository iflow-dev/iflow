# Unified Server Management Scripts

This directory contains the unified server management scripts for all iflow environments. These scripts provide a consistent interface for starting, stopping, checking status, and restarting servers across all environments.

## Script Pattern

All environments now use the unified pattern:
```
/opt/iflow/<env>/server {start|stop|status|restart}
```

## Available Commands

### start
- Starts the server if it's not already running
- **Fails if server is already running** (as requested in ticket #104)
- Automatically handles virtual environment setup
- Installs iflow package if needed
- Sets up database if needed
- Starts server in background

### stop
- Stops the running server gracefully
- Waits for graceful shutdown (up to 10 seconds)
- Force kills if necessary
- Cleans up PID files

### status
- Shows current server status
- Displays PID and port information
- Uses color-coded output for clarity

### restart
- Stops existing server (if running)
- Starts a new server instance
- Useful for applying configuration changes

## Environment-Specific Scripts

### Development Environment
- **Script**: `/opt/iflow/dev/server`
- **Port**: 8080
- **Database**: `.iflow-test`
- **PID File**: `/tmp/iflow-dev.pid`

### QA Environment
- **Script**: `/opt/iflow/qa/server`
- **Port**: 8081
- **Database**: `.iflow-test`
- **PID File**: `/tmp/iflow-qa.pid`

### Production Environment
- **Script**: `/opt/iflow/prod/server`
- **Port**: 9000
- **Database**: `.iflow-demo`
- **PID File**: `/tmp/iflow-prod.pid`

### Integration Environment
- **Script**: `/opt/iflow/integration/server`
- **Port**: 8082
- **Database**: `.iflow-test`
- **PID File**: `/tmp/iflow-integration.pid`

## Usage Examples

```bash
# Check status of all environments
/opt/iflow/dev/server status
/opt/iflow/qa/server status
/opt/iflow/prod/server status
/opt/iflow/integration/server status

# Start development environment
/opt/iflow/dev/server start

# Stop QA environment
/opt/iflow/qa/server stop

# Restart production environment
/opt/iflow/prod/server restart

# Start integration environment
/opt/iflow/integration/server start
```

## Key Features

- **Universal Access**: All scripts can be run from anywhere
- **Background Execution**: Servers start in background using `nohup`
- **PID Management**: Tracks running processes using PID files
- **Port Validation**: Verifies that ports are actually listening
- **Graceful Shutdown**: Attempts graceful shutdown before force kill
- **Color Output**: Uses colors for better readability
- **Error Handling**: Comprehensive error handling and status reporting

## Implementation Details

- **No Redundancy**: Single script per environment (no duplicate functionality)
- **Background Startup**: All servers start in background as requested
- **Fail on Already Running**: Start command fails if server is already running
- **Automatic Setup**: Handles virtual environment and package installation
- **Database Management**: Automatically sets up required databases

## File Locations

The scripts are stored in two locations:
1. **Repository**: `environments/server-scripts/` (for version control)
2. **System**: `/opt/iflow/<env>/server` (for execution)

This ensures the scripts are version controlled while being easily accessible for system operations.
