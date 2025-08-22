#!/usr/bin/env python3
"""
Radish test runner with environment support.

Now only using main_simple().
Always uses port 7000.
Always sets PYTHON_LOG_LEVEL=TRACE.
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
    print("🔧 Initializing temporary database...")
    cmd_init_db = [sys.executable, str(start_server_script), "--init-db", "--output-db-path"]
    try:
        result = subprocess.run(cmd_init_db, capture_output=True, text=True, check=True)
        temp_db_path = result.stdout.strip()
        print(f"✅ Database initialized: {temp_db_path}")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"❌ Failed to initialize database: {e}")
    
    time.sleep(2)
    
    # Start the server with the temp database on port 7000
    cmd = [sys.executable, str(start_server_script),
           "--port", str(DEFAULT_PORT),
           "--database", temp_db_path]
    
    print(f"🚀 Starting server with temp DB: {temp_db_path}")
    process = subprocess.Popen(cmd)
    
    # Wait for server to start
    time.sleep(10)
    
    # Check if server is running
    try:
        import requests
        response = requests.get(f"http://localhost:{DEFAULT_PORT}/api/artifacts", timeout=10)
        if response.status_code == 200:
            print(f"✅ Local server started successfully on port {DEFAULT_PORT}")
            return process
        else:
            raise RuntimeError(f"Server responded with status {response.status_code}")
    except ImportError:
        # If requests is not available, just check if process is still running
        if process.poll() is None:
            print(f"✅ Local server started on port {DEFAULT_PORT} (status check skipped)")
            return process
        else:
            raise RuntimeError("Server process failed to start")
    except Exception as e:
        raise RuntimeError(f"Failed to start local server: {e}")

def stop_local_server(process: subprocess.Popen) -> None:
    """Stop the local server on port 7000 and clean up."""
    if process and process.poll() is None:
        print(f"Stopping local server on port {DEFAULT_PORT}...")
        process.terminate()
        try:
            process.wait(timeout=10)
            print(f"✅ Local server on port {DEFAULT_PORT} stopped")
        except subprocess.TimeoutExpired:
            print(f"⚠️  Server on port {DEFAULT_PORT} didn't stop gracefully, forcing...")
            process.kill()
            process.wait()
            print(f"✅ Local server on port {DEFAULT_PORT} force stopped")
    else:
        print(f"Local server on port {DEFAULT_PORT} is not running")

def setup_python_path() -> None:
    """Set up Python path to include the tests directory."""
    script_dir = get_script_dir()
    tests_dir = script_dir / "tests"
    
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
    
    print(f"Running command: {' '.join(radish_cmd)}")
    
    try:
        result = subprocess.run(radish_cmd, check=False)
        status_code = result.returncode
        print(f"Radish command completed with status code: {status_code}")
        return status_code
    except FileNotFoundError:
        print("Error: 'radish' command not found. Please install radish-bdd.")
        return 1

def main_simple():
    """
    Single entrypoint ignoring typer, always using port 7000, 
    and always runs with PYTHON_LOG_LEVEL=TRACE.
    """
    if len(sys.argv) < 3:
        print("Usage: run_radish.py <environment> <radish_args...>\nExample: run_radish.py local tests/features/")
        sys.exit(1)
    
    # We ignore environment, just read the param to check if 'local' is used
    environment = sys.argv[1]
    radish_args = sys.argv[2:]
    known_args = ["--foreground", "--debug", "--trace", "--local"]
    radish_args = [arg for arg in radish_args if arg not in known_args]
    
    # Hard-coded defaults
    local_mode = (environment == "local")
    
    # Always set trace logging
    os.environ["PYTHON_LOG_LEVEL"] = "TRACE"
    # Always run in visible mode
    os.environ["HEADLESS_MODE"] = "false"
    
    local_server_process = None
    
    def cleanup_local_server(signum=None, frame=None):
        if local_server_process:
            stop_local_server(local_server_process)
        if signum:
            sys.exit(1)
    
    try:
        if local_mode:
            local_server_process = start_local_server()
            os.environ["IFLOW_BASE_URL"] = f"http://localhost:{DEFAULT_PORT}"
            print(f"Using local environment on port {DEFAULT_PORT}")
            print(f"Set IFLOW_BASE_URL=http://localhost:{DEFAULT_PORT}")
        else:
            # dev, qa, prod, etc. all do not matter as we won't override the environment
            # but let's set base url just in case
            env_url = ENVIRONMENT_URLS.get(environment, f"http://localhost:{DEFAULT_PORT}")
            os.environ["IFLOW_BASE_URL"] = env_url
            print(f"Using environment: {environment} => {env_url}")
        
        print("PYTHON_LOG_LEVEL=TRACE (hard-coded)")
        print("HEADLESS_MODE=false (always visible)")
        
        setup_python_path()
        status_code = run_radish(radish_args)
        sys.exit(status_code)
    finally:
        cleanup_local_server()

if __name__ == "__main__":
    main_simple()
