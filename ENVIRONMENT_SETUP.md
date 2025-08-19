# Environment Setup

This document describes the setup and details of all environments used in the iflow project.

## Environments Overview

All environments follow the standard pattern `/opt/iflow/<env>/start.sh` and can be started from anywhere without changing directories.

### Development Environment
- **Working Directory**: `/opt/iflow/dev/`
- **Port**: 8080
- **Database**: `/opt/iflow/dev/.iflow-test`
- **Start Command**: `/opt/iflow/dev/start.sh`
- **Purpose**: Local development and testing

### QA Environment
- **Working Directory**: `/opt/iflow/qa/`
- **Port**: 8081
- **Database**: `/opt/iflow/qa/.iflow-test`
- **Start Command**: `/opt/iflow/qa/start.sh`
- **Purpose**: Quality assurance testing

### Production Environment
- **Working Directory**: `/opt/iflow/prod/`
- **Port**: 9000
- **Database**: `/opt/iflow/prod/.iflow-demo`
- **Start Command**: `/opt/iflow/prod/start.sh`
- **Purpose**: Production deployment

### Integration Environment
- **Working Directory**: `/opt/iflow/integration/`
- **Port**: 8082
- **Database**: `/opt/iflow/integration/.iflow-test`
- **Start Command**: `/opt/iflow/integration/start.sh`
- **Purpose**: Integration testing of multiple PRs

## Key Features

- **Universal Access**: All start scripts can be run from anywhere using `/opt/iflow/<env>/start.sh`
- **Automatic Setup**: Scripts automatically handle virtual environment creation, package installation, and database setup
- **Consistent Pattern**: All environments follow the same startup pattern and structure
- **Port Management**: Each environment uses a unique port to avoid conflicts
- **Database Isolation**: Each environment has its own isolated database

## Usage Examples

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

## Configuration

All environments use the same `config.yaml` file for consistency. Environment-specific settings are handled through environment variables and startup scripts.


