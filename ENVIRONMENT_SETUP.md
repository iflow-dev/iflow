# iflow Environment Setup

## Overview
The iflow project now has four separate environments with proper isolation:

1. **Development Environment** - Runs from source code
2. **QA Environment** - Runs from installed package in dedicated virtual environment
3. **Production Environment** - Runs from installed package in dedicated virtual environment
4. **Integration Environment** - Runs from installed package for testing multiple PRs together

## Environment Details

### 1. Development Environment
- **Working Directory**: `/Users/claudio/realtime/reos2`
- **Port**: 8080
- **Database**: `.iflow-test` (relative to project root)
- **Python Environment**: Uses project's virtual environment
- **Code Source**: Direct source code execution
- **Purpose**: AI development and testing activities

**Start Command**:
```bash
cd /Users/claudio/realtime/reos2
source venv/bin/activate
python sw/iflow/web_server.py --port 8080 --database .iflow-test --host 0.0.0.0
```

### 2. QA Environment
- **Working Directory**: `/opt/iflow/qa/`
- **Port**: 8081
- **Database**: `/opt/iflow/qa/.iflow-test`
- **Python Environment**: Dedicated virtual environment at `/opt/iflow/qa/venv/`
- **Code Source**: Installed iflow package (`pip install .`)
- **Purpose**: Human testing and QA activities

**Start Command**:
```bash
cd /opt/iflow/qa
./start_qa.sh
```

**Manual Start**:
```bash
cd /opt/iflow/qa
source venv/bin/activate
python -m iflow.web_server --port 8081 --database /opt/iflow/qa/.iflow-test --host 0.0.0.0
```

### 3. Production Environment
- **Working Directory**: `/opt/iflow/prod/`
- **Port**: 9000
- **Database**: `/opt/iflow/prod/.iflow-demo`
- **Python Environment**: Dedicated virtual environment at `/opt/iflow/prod/venv/`
- **Code Source**: Installed iflow package (`pip install .`)
- **Purpose**: Production use

**Start Command**:
```bash
cd /opt/iflow/prod
./start_prod.sh
```

**Manual Start**:
```bash
cd /opt/iflow/prod
source venv/bin/activate
python -m iflow.web_server --port 9000 --database /opt/iflow/prod/.iflow-demo --host 0.0.0.0
```

### 4. Integration Environment
- **Working Directory**: `/Users/claudio/realtime/reos2/environments/integration/`
- **Port**: 8082
- **Database**: `.iflow-test` (cloned from GitHub repository)
- **Python Environment**: Dedicated virtual environment at `environments/integration/venv/`
- **Code Source**: Installed iflow package (`pip install .`)
- **Purpose**: Testing multiple pull requests together before merging to main

**Start Command**:
```bash
cd environments/integration
./start_integration.sh
```

**Manual Start**:
```bash
cd environments/integration
source venv/bin/activate
python -m iflow.web_server --port 8082 --database .iflow-test --host 0.0.0.0 --title "iflow - Integration Environment"
```

## Environment Isolation Benefits

1. **Code Isolation**: Changes to source code in development don't affect QA/Production
2. **Package Management**: QA/Production use stable, installed packages
3. **Database Separation**: Each environment has its own database
4. **Virtual Environment Isolation**: Each environment has dedicated Python dependencies
5. **Port Separation**: No conflicts between environments

## Package Installation

The iflow package is installed in QA and Production environments using:
```bash
pip install /Users/claudio/realtime/reos2
```

This installs the package with all dependencies and static files.

## Configuration

All environments use the same `config.yaml` from the project repository, ensuring consistent:
- Artifact types
- Status definitions
- Colors and icons
- Project settings

## Startup Scripts

Both QA and Production environments have startup scripts:
- `/opt/iflow/qa/start_qa.sh`
- `/opt/iflow/prod/start_prod.sh`

These scripts:
- Activate the appropriate virtual environment
- Set environment variables
- Start the web server with correct parameters

## Current Status

- ✅ Development Environment: Running on port 8080
- ✅ QA Environment: Running on port 8081
- ✅ Production Environment: Running on port 9000
- ✅ Integration Environment: Created and ready for use on port 8082
- ✅ All environments serving web interface correctly
- ✅ Static files properly included in installed packages
- ✅ Environment isolation working as intended

## Maintenance

To update QA/Production environments after code changes:
1. Make changes in development environment
2. Test changes thoroughly
3. Reinstall package in QA/Production:
   ```bash
   cd /opt/iflow/qa && source venv/bin/activate && pip install --force-reinstall /Users/claudio/realtime/reos2
   cd /opt/iflow/prod && source venv/bin/activate && pip install --force-reinstall /Users/claudio/realtime/reos2
   ```
4. Restart the respective servers


