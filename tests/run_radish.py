#!/usr/bin/env python3
"""
Radish test runner with environment support.

-   This script will start a local test server on port 7000 (no other port allowed on PURPOSE!)
-   Starting the server and invoking the tests can take up to 15 seconds
-   Running the full test suite can take up to 5 minutes
-   USAGE:
    1.   run smoke tests using a command like:

            tests/run_radish.py local features/* --tags=smoke --trace
    2.  NOTE THAT the directory to the feature files must be relative to tests/ directory as
        in the example 
    3.   REMEMBER: TESTS TAKE A LOT TIME
    4.   BE PATIENT, TESTS TAKE A LONG TIME TO FINISH !!!!!!!!!!!!
"""

import os
import sys
import subprocess
import time
import signal
import atexit
from pathlib import Path
from typing import List
import typer
import logging

# Ensure TRACE log level and a trace() method exist on Logger
TRACE = 15
logging.addLevelName(TRACE, "TRACE")
if not hasattr(logging.Logger, "trace"):
    def _trace(self, message, *args, **kwargs):
        if self.isEnabledFor(TRACE):
            self._log(TRACE, message, args, **kwargs)
    logging.Logger.trace = _trace

logger = logging.getLogger(__name__)

script_dir = os.path.dirname(__file__)

DEFAULT_PORT = 7000

def get_script_dir() -> Path:
    """Get the directory containing this script."""
    return Path(__file__).parent.absolute()

def start_local_server() -> subprocess.Popen:
    """
    Start a local iflow server on port 7000 with a temporary database.
    """
    script_dir = get_script_dir()
    start_server_script = script_dir / "start_server.py"
    
    if not start_server_script.exists():
        raise FileNotFoundError(f"start_server.py not found at {start_server_script}")
    
    # Initialize the temp database synchronously
    logger.trace("🔧 Initializing temporary database...")
    cmd_init_db = [sys.executable, str(start_server_script), "--init-db", "--output-db-path"]
    try:
        # Run init command in the tests directory so relative paths resolve correctly
        result = subprocess.run(cmd_init_db, capture_output=True, text=True, check=True, cwd=script_dir)
        temp_db_path = (result.stdout or "").strip()
        if not temp_db_path:
            # If stdout is empty, try stderr as a fallback for integration with different runners
            temp_db_path = (result.stderr or "").strip()
        if not temp_db_path:
            raise RuntimeError(f"Init-db command did not return a database path. stdout={result.stdout!r} stderr={result.stderr!r}")
        logger.trace(f"✅ Database initialized: {temp_db_path}")
    except subprocess.CalledProcessError as e:
        # Provide stderr in the error for easier debugging
        raise RuntimeError(f"❌ Failed to initialize database: {e}; stderr={e.stderr!r}")
    
    time.sleep(2)
    
    # Start the server with the temp database on port 7000
    cmd = [sys.executable, str(start_server_script),
           "--port", str(DEFAULT_PORT),
           "--database", temp_db_path]
    
    logger.trace(f"🚀 Starting server with temp DB: {temp_db_path}")
    # Start the server in the tests directory so the server uses local repo files
    process = subprocess.Popen(cmd, cwd=script_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Wait for server to start
    time.sleep(10)
    
    # Check if server is running
    try:
        import requests
        response = requests.get(f"http://localhost:{DEFAULT_PORT}/api/artifacts", timeout=10)
        if response.status_code == 200:
            logger.trace(f"✅ Local server started successfully on port {DEFAULT_PORT}")
            return process
        else:
            raise RuntimeError(f"Server responded with status {response.status_code}")
    except ImportError:
        # If requests is not available, just check if process is still running
        if process.poll() is None:
            logger.trace(f"✅ Local server started on port {DEFAULT_PORT} (status check skipped)")
            return process
        else:
            raise RuntimeError("Server process failed to start")
    except Exception as e:
        raise RuntimeError(f"Failed to start local server: {e}")

def stop_local_server(process: subprocess.Popen) -> None:
    """Stop the local server on port 7000 and clean up."""
    if process and process.poll() is None:
        logger.trace(f"Stopping local server on port {DEFAULT_PORT}...")
        process.terminate()
        try:
            process.wait(timeout=10)
            logger.trace(f"✅ Local server on port {DEFAULT_PORT} stopped")
        except subprocess.TimeoutExpired:
            logger.trace(f"⚠️  Server on port {DEFAULT_PORT} didn't stop gracefully, forcing...")
            process.kill()
            process.wait()
            logger.trace(f"✅ Local server on port {DEFAULT_PORT} force stopped")
    else:
        logger.trace(f"Local server on port {DEFAULT_PORT} is not running")

def setup_python_path() -> None:
    """Set up Python path to include the tests directory."""
    script_dir = get_script_dir()
    tests_dir = script_dir / "support"
    
    current_pythonpath = os.environ.get("PYTHONPATH", "")
    if current_pythonpath:
        new_pythonpath = f"{tests_dir}:{current_pythonpath}"
    else:
        new_pythonpath = str(tests_dir)
    
    os.environ["PYTHONPATH"] = new_pythonpath


def run_radish(args: List[str]) -> int:
    """
    Run the radish command with the given arguments and return the status code.
    """
    # Build the radish command
    args.append("-t")
    radish_cmd = ["radish"] + args
    
    logger.trace(f"Running command: {' '.join(radish_cmd)}")
    
    try:
        result = subprocess.run("source ../venv-local/bin/activate && " + " ".join(radish_cmd),
                                check=False, cwd=script_dir, shell=True)
        status_code = result.returncode
        logger.trace(f"Radish command completed with status code: {status_code}")
        return status_code
    except FileNotFoundError:
        logger.trace("Error: 'radish' command not found. Please install radish-bdd.")
        return 1

def main_simple():
    """
    Single entrypoint ignoring typer, always using port 7000, 
    and always runs with PYTHON_LOG_LEVEL=TRACE.
    """
    if len(sys.argv) < 3:
        logger.trace("Usage: run_radish.py <environment> <radish_args...>\nExample: run_radish.py local tests/features/")
        sys.exit(1)
    
    # We ignore environment, just read the param to check if 'local' is used
    environment = sys.argv[1]
    radish_args = sys.argv[2:]
    
    # Check for --foreground and --dry-run before filtering other known args
    foreground_mode = "--foreground" in radish_args
    dry_run_mode = "--dry-run" in radish_args
    
    # Filter out known args including --foreground and --dry-run (since we handle them separately)
    known_args = ["--foreground", "--debug", "--trace", "--local", "--dry-run"]
    radish_args = [arg for arg in radish_args if arg not in known_args]
    
    logger.trace(f"DEBUG: After filtering, radish_args: {radish_args}")
    
    # Hard-coded defaults
    local_mode = (environment == "local")
    
    # Always set trace logging
    os.environ["PYTHON_LOG_LEVEL"] = "TRACE"
    
    # Set headless mode based on --foreground flag
    if foreground_mode:
        os.environ["HEADLESS_MODE"] = "false"
        logger.trace("HEADLESS_MODE=false (foreground mode enabled)")
    else:
        os.environ["HEADLESS_MODE"] = "true"
        logger.trace("HEADLESS_MODE=true (headless mode enabled)")
    
    local_server_process = None
    
    def cleanup_local_server(signum=None, frame=None):
        if local_server_process:
            stop_local_server(local_server_process)
        if signum:
            sys.exit(1)
    
    try:
        if dry_run_mode:
            # Skip server startup for dry-run mode
            logger.trace("🏃‍♂️ DRY-RUN MODE: Skipping server startup")
            os.environ["IFLOW_BASE_URL"] = f"http://localhost:{DEFAULT_PORT}"
            logger.trace(f"Set IFLOW_BASE_URL=http://localhost:{DEFAULT_PORT} (dry-run)")
        elif local_mode:
            local_server_process = start_local_server()
            os.environ["IFLOW_BASE_URL"] = f"http://localhost:{DEFAULT_PORT}"
            logger.trace(f"Using local environment on port {DEFAULT_PORT}")
            logger.trace(f"Set IFLOW_BASE_URL=http://localhost:{DEFAULT_PORT}")
        else:
            # dev, qa, prod, etc. all do not matter as we won't override the environment
            # but let's set base url just in case
            env_url = f"http://localhost:{DEFAULT_PORT}"
            os.environ["IFLOW_BASE_URL"] = env_url
            logger.trace(f"Using environment: {environment} => {env_url}")
        
        logger.trace("PYTHON_LOG_LEVEL=TRACE (hard-coded)")
        
        setup_python_path()
        
        # Add --dry-run flag back to radish args if dry-run mode is enabled
        if dry_run_mode:
            radish_args.append("--dry-run")
            logger.trace(f"🔍 Adding --dry-run to radish command")
        
        status_code = run_radish(radish_args)
        sys.exit(status_code)
    finally:
        cleanup_local_server()

if __name__ == "__main__":
    main_simple()
