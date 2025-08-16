# iflow

A tool for managing project artifacts like requirements, tasks, test cases, and issues for projects.

## Overview

iflow is a Python-based project artifact management tool that provides a web-based interface using pywebview. It stores all project information in artifacts with a YAML-like structure and maintains full history through git-based storage.

## Features

- **Artifact Management**: Create, read, update, and delete project artifacts
- **Multiple Artifact Types**: Support for requirements, tasks, test cases, issues, bugs, features, and stories
- **Git-based Storage**: Full version control and history tracking for all artifacts
- **Web-based Interface**: Modern, responsive UI built with HTML/CSS/JavaScript
- **Search and Filter**: Find artifacts by text or filter by type
- **Statistics Dashboard**: View project metrics and git status
- **Cross-platform**: Works on Windows, macOS, and Linux

## Architecture

- **Flat Structure**: All artifacts are stored in a flat file structure
- **Git Database**: Each artifact is stored as a YAML file with full git history
- **Artifact Format**: YAML-like structure with metadata, summary, and description
- **Web Interface**: pywebview provides the desktop application wrapper

## Installation

### Prerequisites

- Python 3.8 or higher
- Git (for version control)

### Install from source

```bash
# Clone the repository
git clone <repository-url>
cd iflow

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

### Install dependencies only

```bash
pip install pywebview PyYAML GitPython
```

## Usage

### Command Line

```bash
# Run with default database path (.iflow)
iflow

# Run with custom database path
iflow --database ./my-project

# Show help
iflow --help
```

### Python API

```python
from iflow import IFlowApp

# Create and run the application
app = IFlowApp(database_path=".iflow")
app.run()
```

### Creating Artifacts Programmatically

```python
from iflow import Artifact, ArtifactType, GitDatabase

# Create a database
db = GitDatabase(".iflow")

# Create an artifact
requirement = Artifact(
    artifact_type=ArtifactType.REQUIREMENT,
    summary="User authentication system",
    description="Implement secure user login and registration"
)

# Save to database
db.save_artifact(requirement)
```

## Artifact Structure

Each artifact follows this YAML structure:

```yaml
artifact:
    id: <unique_id>
    type: requirement
    summary: <summary>
    description: <details>
    created_at: <timestamp>
    updated_at: <timestamp>
    metadata: {}
```

## Supported Artifact Types

- **requirement**: Project requirements and specifications
- **task**: Development tasks and work items
- **test_case**: Test cases and testing scenarios
- **issue**: General project issues
- **bug**: Software bugs and defects
- **feature**: New features and enhancements
- **story**: User stories and use cases

## Database Operations

The GitDatabase class provides these operations:

- `save_artifact(artifact)`: Save a new artifact
- `get_artifact(artifact_id)`: Retrieve an artifact by ID
- `list_artifacts(type=None)`: List all artifacts, optionally filtered by type
- `update_artifact(artifact)`: Update an existing artifact
- `delete_artifact(artifact_id)`: Delete an artifact
- `search_artifacts(query)`: Search artifacts by text
- `get_artifact_history(artifact_id)`: Get git history for an artifact
- `get_stats()`: Get database statistics

## Web Interface

The web interface provides:

- **Dashboard**: Overview of all artifacts with statistics
- **Create/Edit**: Modal forms for creating and editing artifacts
- **Search**: Text-based search across all artifacts
- **Filtering**: Filter artifacts by type
- **Responsive Design**: Works on different screen sizes
- **Modern UI**: Clean, professional appearance

## Development

### Project Structure

```
iflow/
├── __init__.py          # Package initialization
├── core.py              # Core classes (Artifact, ArtifactType)
├── database.py          # Git-based database operations
├── app.py               # Main application and web interface
├── main.py              # Command-line entry point
├── setup.py             # Package setup and installation
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

### Running Tests

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=iflow
```

### Code Quality

```bash
# Format code
black iflow/

# Lint code
flake8 iflow/

# Type checking
mypy iflow/
```

## Dependencies

### Core Dependencies

- **pywebview**: Desktop application wrapper for web technologies
- **PyYAML**: YAML parsing and generation
- **GitPython**: Git repository operations

### Development Dependencies

- **pytest**: Testing framework
- **pytest-cov**: Coverage reporting
- **black**: Code formatting
- **flake8**: Code linting
- **mypy**: Type checking

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Roadmap

- [ ] Export/import functionality
- [ ] Advanced search and filtering
- [ ] Artifact relationships and dependencies
- [ ] Team collaboration features
- [ ] Integration with external tools
- [ ] Mobile-responsive web interface
- [ ] Plugin system for custom artifact types

## Support

For questions, issues, or contributions, please:

1. Check the existing issues
2. Create a new issue with detailed information
3. Provide steps to reproduce any problems
4. Include system information and Python version

## Acknowledgments

- Built with [pywebview](https://pywebview.flowrl.com/) for the desktop interface
- Uses [GitPython](https://gitpython.readthedocs.io/) for git operations
- Inspired by modern project management tools and methodologies
