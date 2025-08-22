#!/usr/bin/env python3
"""
Simple script to start a local iflow web server.

REQUIREMENTS:
- Port range: 7000-7100 (automatically finds free port)
- --init-db: Creates database in /tmp using tempfile.mkdtemp()
- Port checking: Verifies port is free before starting
- Error handling: Returns exit code > 0 on error with proper logging
- Directory independence: Works from any directory, manages Python path itself
- Environment override: Uses local directories, overrides any Python environment
- No virtual environment dependencies
- --trace: Enable TRACE level logging (level 15) for detailed function tracing

SCRIPT REQUIREMENTS:
- Starting a local server from any directory
- Checking if the port is free and abort with error and status 1
- Port range 7000-7100
- Run with --init-db on a /tmp/ directory using tmpname
- Using local changes from local repo without any virtual environment
- Auto-find free port in range if no port specified
- Database path validation and fallback to .iflow-local
- Git repository initialization with initial artifact
- Static folder override to use local files
- Comprehensive error handling with exit codes
- Logging with timestamps and levels
- TRACE level logging for function tracing

Usage:
    python start_server.py [--port PORT] [--database PATH] [--init-db] [--trace]
    
    Options:
        --port PORT        Port to run the server on (default: auto-find in 7000-7100)
        --database PATH    Path to the database to use for this instance
        --init-db          Initialize a new database in /tmp
        --trace            Enable TRACE level logging (level 15) for detailed function tracing
"""
import sys
import os
import argparse
import socket
import tempfile
import logging
import subprocess
from pathlib import Path

# Define custom TRACE level (15) - between DEBUG (10) and INFO (20)
TRACE = 15
logging.addLevelName(TRACE, 'TRACE')

def trace(self, message, *args, **kwargs):
    """Add trace method to logger if it doesn't exist."""
    if self.isEnabledFor(TRACE):
        self._log(TRACE, message, args, **kwargs)

# Add trace method to Logger class if it doesn't exist
if not hasattr(logging.Logger, 'trace'):
    logging.Logger.trace = trace

# Configure logging (will be overridden if output-db-path is used)
logger = logging.getLogger(__name__)

def setup_environment():
    """Set up Python environment to use local files regardless of current directory."""
    logger.trace("Setting up Python environment...")
    
    # Get the absolute path to the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Add the sw directory to Python path
    sw_path = os.path.join(script_dir, 'sw')
    if not os.path.exists(sw_path):
        logger.error(f"sw directory not found at: {sw_path}")
        logger.error(f"Current working directory: {os.getcwd()}")
        logger.error(f"Script location: {script_dir}")
        sys.exit(1)
    
    # Insert sw path at the beginning to override any installed packages
    # This ensures local repo changes take priority over virtual environment packages
    sys.path.insert(0, sw_path)
    
    # Change to sw directory so relative imports work
    os.chdir(sw_path)
    logger.trace(f"Changed working directory to: {sw_path}")
    logger.trace(f"Python path: {sys.path[:3]}")

def find_free_port(start_port=7000, end_port=7100):
    """Find a free port in the specified range."""
    logger.trace(f"Searching for free port in range {start_port}-{end_port}")
    for port in range(start_port, end_port + 1):
        if is_port_free(port):
            logger.trace(f"Found free port: {port}")
            return port
    logger.trace("No free ports found in specified range")
    return None

def is_port_free(port):
    """Check if a port is free to use."""
    logger.trace(f"Checking if port {port} is free")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('localhost', port))
            logger.trace(f"Port {port} is free")
            return True
        except OSError:
            logger.trace(f"Port {port} is not free")
            return False

def create_temp_database():
    """Create a temporary database directory with proper state tagging."""
    logger.trace("Creating temporary database directory...")
    try:
        import uuid
        temp_dir = f"/tmp/{uuid.uuid4()}.database"
        os.makedirs(temp_dir, exist_ok=True)
        logger.trace(f"Created temporary database directory: {temp_dir}")
        
        # Initialize git repository first (empty state)
        logger.info(f"Initializing git repository in {temp_dir}")
        try:
            subprocess.run(['git', 'init'], cwd=temp_dir, check=True, capture_output=True, text=True)
            # Tag empty state as "zero"
            subprocess.run(['git', 'commit', '--allow-empty', '-m', 'Empty database state'], cwd=temp_dir, check=True, capture_output=True, text=True)
            subprocess.run(['git', 'tag', 'zero'], cwd=temp_dir, check=True, capture_output=True, text=True)
            logger.info("Tagged empty state as 'zero'")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to initialize git repository: {e}")
            logger.error(f"Git output: {e.stderr}")
            sys.exit(1)
        except FileNotFoundError:
            logger.error("Git not found. Please install git.")
            sys.exit(1)
        
        return temp_dir
    except Exception as e:
        logger.error(f"Failed to create temporary database: {e}")
        sys.exit(1)

def init_database(database_path):
    """Initialize a new iflow database with git repository and initial artifacts."""
    try:
        import yaml
    except ImportError:
        logger.error("PyYAML not available. Install with: pip install pyyaml")
        sys.exit(1)
    
    db_path = Path(database_path)
    
    # Create database directory if it doesn't exist
    db_path.mkdir(parents=True, exist_ok=True)
    
    # Initialize git repository
    logger.info(f"Initializing git repository in {db_path}")
    try:
        subprocess.run(['git', 'init'], cwd=db_path, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to initialize git repository: {e}")
        logger.error(f"Git output: {e.stderr}")
        sys.exit(1)
    except FileNotFoundError:
        logger.error("Git not found. Please install git.")
        sys.exit(1)
    
    # Create artifacts subdirectory
    artifacts_dir = db_path / 'artifacts'
    artifacts_dir.mkdir(exist_ok=True)
    logger.info(f"Created artifacts directory: {artifacts_dir}")
    
    # Create initial artifact 00001.yaml in artifacts/ subdirectory
    initial_artifact = {
        'artifact': {
            'id': '00001',
            'type': 'requirement',
            'summary': 'Initial requirement',
            'description': 'This is the first artifact created when initializing the database.',
            'status': 'open',
            'category': 'system',
            'created_at': '2025-08-20T00:00:00.000000',
            'updated_at': '2025-08-20T00:00:00.000000',
            'verification': 'NONE',
            'flagged': False,
            'metadata': {}
        }
    }
    
    artifact_file = artifacts_dir / '00001.yaml'
    try:
        with open(artifact_file, 'w') as f:
            yaml.dump(initial_artifact, f, default_flow_style=False)
            logger.info(f"Created initial artifact: {artifact_file}")
    except Exception as e:
        logger.error(f"Failed to create initial artifact: {e}")
        sys.exit(1)
    
    # Add and commit the artifact
    try:
        subprocess.run(['git', 'add', 'artifacts/00001.yaml'], cwd=db_path, check=True, capture_output=True, text=True)
        subprocess.run(['git', 'commit', '-m', 'Initial artifact: Initial requirement'], cwd=db_path, check=True, capture_output=True, text=True)
        subprocess.run(['git', 'tag', 'v0.0.0'], cwd=db_path, check=True, capture_output=True, text=True)
        subprocess.run(['git', 'tag', 'base'], cwd=db_path, check=True, capture_output=True, text=True)
        
        # Reset master branch to point to base tag
        subprocess.run(['git', 'reset', '--hard', 'base'], cwd=db_path, check=True, capture_output=True, text=True)
        logger.info("Master branch now points to 'base' tag")
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to commit initial artifact: {e}")
        logger.error(f"Git output: {e.stderr}")
        # Don't exit here, the database is still usable
    
    logger.info("Database initialization completed successfully!")
    logger.info(f"Database location: {db_path.absolute()}")
    logger.info("Initial artifact: 00001.yaml")
    logger.info("Git tags: v0.0.0, base")

def main():
    parser = argparse.ArgumentParser(description='Start iflow web server')
    parser.add_argument('--port', type=int, help='Port to run the server on (default: auto-find in 7000-7100)')
    parser.add_argument('--database', type=str, help='Path to the database to use for this instance')
    parser.add_argument('--init-db', action='store_true', help='Initialize a new database in /tmp')
    parser.add_argument('--output-db-path', action='store_true', help='Output database path to stdout (for integration)')
    parser.add_argument('--trace', action='store_true', help='Enable TRACE level logging (level 15) for detailed function tracing')
    
    args = parser.parse_args()
    
    # Configure logging based on arguments
    if args.output_db_path:
        # For path output, redirect logging to stderr
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stderr)
            ]
        )
    else:
        # Normal logging to stdout
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout)
            ]
        )
    
    # Set up environment first
    setup_environment()
    
    # Handle database path
    if args.init_db:
        if args.database:
            logger.warning("--init-db specified, ignoring --database argument")
        database_path = create_temp_database()
        logger.info(f"Using temporary database: {database_path}")
    elif args.database:
        database_path = args.database
        logger.info(f"Using specified database: {database_path}")
    else:
        # No fallback - require explicit database path or init-db
        logger.error("No database specified. Use --database PATH or --init-db")
        sys.exit(1)
    
    # Initialize database if requested (do this before output)
    if args.init_db:
        logger.info("Initializing new database...")
        init_database(database_path)
    
    # Output database path if requested (for integration)
    if args.output_db_path:
        print(database_path, flush=True)
        return
    
    # Handle port selection
    if args.port:
        if args.port < 7000 or args.port > 7100:
            logger.error(f"Port {args.port} is outside allowed range (7000-7100)")
            sys.exit(1)
        if not is_port_free(args.port):
            logger.error(f"Port {args.port} is already in use")
            sys.exit(1)
        port = args.port
        logger.info(f"Using specified port: {port}")
    else:
        port = find_free_port()
        if not port:
            logger.error("No free ports found in range 7000-7100")
            sys.exit(1)
        logger.info(f"Auto-selected free port: {port}")
    
    try:
        # Set database path environment variable (no fallback)
        os.environ["IFLOW_DATABASE_PATH"] = database_path
        logger.info(f"Set IFLOW_DATABASE_PATH={database_path}")
        
        # Import after environment setup
        from iflow.web_server import app
        logger.info(f"Starting iflow web server on http://localhost:{port}")
        logger.info(f"Using database: {database_path}")
        
        # Override static folder to use local files
        static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sw', 'iflow', 'static')
        app.static_folder = static_folder
        logger.info(f"Using local static folder: {static_folder}")
        
        # Verify static folder exists
        if not os.path.exists(static_folder):
            logger.error(f"Static folder not found: {static_folder}")
            sys.exit(1)
        
        # Start the server
        logger.info("Server starting...")
        app.run(host='0.0.0.0', port=port, debug=True, use_reloader=False)
        
    except ImportError as e:
        logger.error(f"Import error: {e}")
        logger.error("Make sure you're in the correct directory and dependencies are installed")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
