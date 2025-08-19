# Unified Server Management Scripts

This directory contains the unified server management scripts for all iflow environments. These scripts provide a consistent interface for starting, stopping, checking status, and restarting servers across all environments.

## Architecture

The new implementation uses a **generic Python script** with **environment-specific configuration files**:

- **Generic Script**: `server.py` - Single Python script for all environments
- **Configuration Files**: `.server.yaml` files in each environment directory
- **Wrapper Scripts**: Simple bash wrappers that call the generic Python script

## Script Pattern

All environments use the unified pattern:
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

## Environment-Specific Configuration

Each environment has a `.server.yaml` configuration file:

### Development Environment
- **Script**: `/opt/iflow/dev/server`
- **Config**: `/opt/iflow/dev/.server.yaml`
- **Port**: 8080
- **Database**: `.iflow-test`
- **PID File**: `/tmp/iflow-dev.pid`

### QA Environment
- **Script**: `/opt/iflow/qa/server`
- **Config**: `/opt/iflow/qa/.server.yaml`
- **Port**: 8081
- **Database**: `.iflow-test`
- **PID File**: `/tmp/iflow-qa.pid`

### Production Environment
- **Script**: `/opt/iflow/prod/server`
- **Config**: `/opt/iflow/prod/.server.yaml`
- **Port**: 9000
- **Database**: `.iflow-demo`
- **PID File**: `/tmp/iflow-prod.pid`

### Integration Environment
- **Script**: `/opt/iflow/integration/server`
- **Config**: `/opt/iflow/integration/.server.yaml`
- **Port**: 8082
- **Database**: `.iflow-test`
- **PID File**: `/tmp/iflow-integration.pid`

## Configuration File Format

Each `.server.yaml` file contains:

```yaml
name: dev
port: 8080
database: .iflow-test
database_url: https://github.com/iflow-dev/iflow-test-db.git
```

## Usage Examples

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

## Key Features

- **Generic Implementation**: Single Python script for all environments
- **Configuration-Driven**: Environment-specific settings in YAML files
- **Universal Access**: All scripts can be run from anywhere
- **Background Execution**: Servers start in background using subprocess
- **PID Management**: Tracks running processes using PID files
- **Port Validation**: Verifies that ports are actually listening
- **Graceful Shutdown**: Attempts graceful shutdown before force kill
- **Color Output**: Uses colors for better readability
- **Error Handling**: Comprehensive error handling and status reporting

## Implementation Details

- **No Redundancy**: Single generic script per environment (no duplicate functionality)
- **Background Startup**: All servers start in background as requested
- **Fail on Already Running**: Start command fails if server is already running
- **Automatic Setup**: Handles virtual environment and package installation
- **Database Management**: Automatically sets up required databases
- **Cross-Platform**: Python implementation works on multiple platforms

## File Locations

The scripts are stored in multiple locations:
1. **Generic Script**: `environments/server-scripts/server.py` (for version control)
2. **Configuration Files**: `environments/server-scripts/*-server.yaml` (for version control)
3. **System Scripts**: `/opt/iflow/<env>/server` (for execution)
4. **System Configs**: `/opt/iflow/<env>/.server.yaml` (for execution)

This ensures the scripts are version controlled while being easily accessible for system operations.

## Dependencies

The generic Python script requires:
- Python 3.x
- PyYAML package (for configuration file parsing)
- Standard library modules (os, sys, time, signal, subprocess, argparse, pathlib)

## Testing

All functionality has been tested:
- ✅ Start command fails when server already running
- ✅ Stop command gracefully shuts down servers
- ✅ Status command shows accurate server state
- ✅ Restart command properly cycles servers
- ✅ Background execution with PID tracking
- ✅ Configuration file loading and parsing
