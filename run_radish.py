#!/usr/bin/env python3
"""
Radish test runner with environment support.

This script provides a convenient way to run Radish BDD tests with automatic
environment configuration and Python path setup.
"""

import os
import sys
import subprocess
import time
import signal
import atexit
import argparse
from pathlib import Path
from typing import List, Optional

# Environment URL mappings
ENVIRONMENT_URLS = {
    "dev": "http://localhost:8080",
    "qa": "http://localhost:8081", 
    "prod": "http://localhost:9000"
}

def get_script_dir() -> Path:
    """Get the directory containing this script."""
    return Path(__file__).parent.absolute()

def find_available_port() -> int:
    """Check if port 7000 is available, fail if not."""
    import socket
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', 7000))
            return 7000
    except OSError:
        raise RuntimeError("Port 7000 is already in use. Please stop any running servers and try again.")

def start_local_server(port: int = None) -> subprocess.Popen:
    """Start a local iflow server with temporary database."""
    if port is not None:
        raise RuntimeError("--port is deprecated, don't use! Port 7000 is fixed.")
    
    script_dir = get_script_dir()
    start_server_script = script_dir / "start_server.py"
    
    if not start_server_script.exists():
        raise FileNotFoundError(f"start_server.py not found at {start_server_script}")
    
    # First, initialize the temp database synchronously
    print("🔧 Initializing temporary database...")
    cmd_init_db = [sys.executable, str(start_server_script), "--init-db", "--output-db-path"]
    try:
        result = subprocess.run(cmd_init_db, capture_output=True, text=True, check=True)
        temp_db_path = result.stdout.strip()
        print(f"✅ Database initialized: {temp_db_path}")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"❌ Failed to initialize database: {e}")
    
    # Wait for DB init to complete
    time.sleep(2)
    
    # Start the server with the temp database (no fallback)
    cmd = [sys.executable, str(start_server_script), "--port", "7000", "--database", temp_db_path]
    
    print(f"🚀 Starting server with temp DB: {temp_db_path}")
    
    process = subprocess.Popen(cmd)
    
    # Wait for server to start
    time.sleep(10)
    
    # Check if server is running
    try:
        import requests
        response = requests.get("http://localhost:7000/api/artifacts", timeout=10)
        if response.status_code == 200:
            print("✅ Local server started successfully on port 7000")
            return process
        else:
            raise RuntimeError(f"Server responded with status {response.status_code}")
    except ImportError:
        # If requests is not available, just check if process is still running
        if process.poll() is None:
            print("✅ Local server started on port 7000 (status check skipped)")
            return process
        else:
            raise RuntimeError("Server process failed to start")
    except Exception as e:
        raise RuntimeError(f"Failed to start local server: {e}")

def stop_local_server(process: subprocess.Popen) -> None:
    """Stop the local server and clean up."""
    if process and process.poll() is None:
        print("Stopping local server on port 7000...")
        process.terminate()
        try:
            process.wait(timeout=10)
            print("✅ Local server on port 7000 stopped")
        except subprocess.TimeoutExpired:
            print("⚠️  Server didn't stop gracefully, forcing...")
            process.kill()
            process.wait()
            print("✅ Local server on port 7000 force stopped")
    else:
        print("Local server on port 7000 is not running")

def setup_environment(environment: str, foreground: bool = False, debug: bool = False, trace: bool = False) -> None:
    """Set up environment variables for the specified environment."""
    if environment not in ENVIRONMENT_URLS:
        print(f"Error: Invalid environment '{environment}'. Must be one of: {', '.join(ENVIRONMENT_URLS.keys())}")
        sys.exit(1)
    
    url = ENVIRONMENT_URLS[environment]
    os.environ["IFLOW_BASE_URL"] = url
    
    # Set logging level based on flags (TRACE takes precedence over DEBUG)
    if trace:
        os.environ["PYTHON_LOG_LEVEL"] = "TRACE"
    elif debug:
        os.environ["PYTHON_LOG_LEVEL"] = "DEBUG"
    else:
        os.environ["PYTHON_LOG_LEVEL"] = "INFO"
    
    # Set headless mode based on foreground flag
    if foreground:
        os.environ["HEADLESS_MODE"] = "false"  # Disable headless mode for debugging
        headless_message = "false (Chrome will be visible)"
    else:
        os.environ["HEADLESS_MODE"] = "true"  # Enable headless mode
        headless_message = "true (Chrome will run in headless mode)"
    
    print(f"Using environment: {environment} (URL: {url})")
    print(f"Set IFLOW_BASE_URL={url}")
    print(f"Set PYTHON_LOG_LEVEL={'TRACE' if trace else 'DEBUG' if debug else 'INFO'}")
    print(f"Set HEADLESS_MODE={headless_message}")

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
    """Run the radish command with the given arguments and return the status code."""
    script_dir = get_script_dir()
    tests_dir = script_dir / "tests"
    
    # Check if --basedir or -b is already provided
    has_basedir = any(arg in ["--basedir", "-b"] for arg in args)
    
    # Build the radish command
    radish_cmd = ["radish"] + args
    if not has_basedir:
        radish_cmd.extend(["-b", str(tests_dir)])
    
    print(f"Running command: {' '.join(radish_cmd)}")
    
    # Run the command
    try:
        result = subprocess.run(radish_cmd, check=False)
        status_code = result.returncode
        print(f"Radish command completed with status code: {status_code}")
        return status_code
    except FileNotFoundError:
        print("Error: 'radish' command not found. Please install radish-bdd.")
        return 1

def main():
    """
    Run Radish BDD tests with environment configuration.
    
    The environment parameter is required and must be one of: dev, qa, prod.
    Use --local flag to automatically start a local server with temporary database.
    Use --debug flag to enable debug logging (sets PYTHON_LOG_LEVEL=DEBUG).
    Use --trace flag to enable TRACE level logging (sets PYTHON_LOG_LEVEL=TRACE).
    
    All other arguments are passed directly to the radish command.
    
    Examples:
        run_radish.py dev tests/features/artifact_management.feature
        run_radish.py qa --tags=smoke
        run_radish.py prod tests/features/ --verbose
        run_radish.py dev tests/features/test_status_filtering.feature --foreground
        run_radish.py local tests/features/ --tags=smoke --local
        run_radish.py local tests/features/test_artifact_creation.feature --local --foreground
        run_radish.py local tests/features/ --tags=smoke --local --debug
        run_radish.py local tests/features/ --tags=smoke --local --trace
    """
    
    # Parse arguments using argparse
    parser = argparse.ArgumentParser(
        description="Run Radish BDD tests with environment configuration",
        add_help=False  # We'll handle help manually to pass unknown args to radish
    )
    
    parser.add_argument("environment", help="Environment to run tests against (dev, qa, prod, or 'local' for auto-started server)")
    parser.add_argument("--foreground", "-f", action="store_true", help="Run tests in foreground mode (Chrome will be visible)")
    parser.add_argument("--local", "-l", action="store_true", help="Automatically start a local server with temporary database and run tests against it")
    parser.add_argument("--debug", "-d", action="store_true", help="Enable debug logging (sets PYTHON_LOG_LEVEL=DEBUG)")
    parser.add_argument("--trace", "-t", action="store_true", help="Enable TRACE level logging (sets PYTHON_LOG_LEVEL=TRACE for detailed function tracing)")
    parser.add_argument("--help", "-h", action="store_true", help="Show this help message")
    
    # Parse known args, leaving unknown args for radish
    args, radish_args = parser.parse_known_args()
    
    # Handle help
    if args.help:
        parser.print_help()
        print("\nAll other arguments are passed directly to the radish command.")
        print("\nExamples:")
        print("  run_radish.py dev tests/features/ --tags=smoke")
        print("  run_radish.py local tests/features/ --tags=smoke --local --verbose")
        print("  run_radish.py qa tests/features/ --foreground --dry-run")
        sys.exit(0)
    
    local_server_process = None
    local_port = None
    
    try:
        if args.local:
            # Override environment to 'local' when using --local flag
            args.environment = "local"
            
            # Start local server on fixed port 7000
            local_server_process = start_local_server()
            
            # Set up environment variables for local server
            os.environ["IFLOW_BASE_URL"] = "http://localhost:7000"
            
            # Set logging level based on flags (TRACE takes precedence over DEBUG)
            if args.trace:
                os.environ["PYTHON_LOG_LEVEL"] = "TRACE"
            elif args.debug:
                os.environ["PYTHON_LOG_LEVEL"] = "DEBUG"
            else:
                os.environ["PYTHON_LOG_LEVEL"] = "INFO"
                
            os.environ["HEADLESS_MODE"] = "false" if args.foreground else "true"
            
            print(f"Using local environment (URL: http://localhost:7000)")
            print(f"Set IFLOW_BASE_URL=http://localhost:7000")
            print(f"Set PYTHON_LOG_LEVEL={'TRACE' if args.trace else 'DEBUG' if args.debug else 'INFO'}")
            print(f"Set HEADLESS_MODE={'false (Chrome will be visible)' if args.foreground else 'true (Chrome will run in headless mode)'}")
        else:
            # Set up environment normally
            setup_environment(args.environment, args.foreground, args.debug, args.trace)
        
        # Set up Python path
        setup_python_path()
        
        # Run radish with all remaining arguments and get status code
        status_code = run_radish(radish_args)
        
        # Exit with the radish status code
        sys.exit(status_code)
        
    finally:
        # Clean up local server if it was started
        if local_server_process:
            stop_local_server(local_server_process)

def main_simple():
    """Simple version that doesn't use argparse for argument parsing."""
    if len(sys.argv) < 3:
        print("Usage: run_radish.py <environment> <radish_args...> [--foreground] [--local] [--debug] [--trace]")
        print("Example: run_radish.py dev tests/features/ --tags=smoke")
        print("Example: run_radish.py dev tests/features/test_status_filtering.feature --foreground")
        print("Example: run_radish.py local tests/features/ --tags=smoke --local")
        print("Example: run_radish.py local tests/features/test_artifact_creation.feature --local --foreground")
        print("Example: run_radish.py local tests/features/ --tags=smoke --local --debug")
        print("Example: run_radish.py local tests/features/ --tags=smoke --local --trace")
        sys.exit(1)
    
    environment = sys.argv[1]
    radish_args = sys.argv[2:]
    
    # Check for flags (but don't remove them - pass all to radish)
    foreground = "--foreground" in radish_args
    local = "--local" in radish_args
    debug = "--debug" in radish_args
    trace = "--trace" in radish_args
    
    local_server_process = None
    local_port = None
    
    def cleanup_local_server(signum=None, frame=None):
        """Clean up local server on signal or exit."""
        if local_server_process:
            stop_local_server(local_server_process)
        if signum:
            sys.exit(1)
    
    try:
        if local:
            # Override environment to 'local' when using --local flag
            environment = "local"
            
            # Start local server on fixed port 7000
            local_server_process = start_local_server()
            
            # Set up signal handlers for cleanup
            signal.signal(signal.SIGINT, cleanup_local_server)
            signal.signal(signal.SIGTERM, cleanup_local_server)
            atexit.register(cleanup_local_server)
            
            # Set up environment variables for local server
            os.environ["IFLOW_BASE_URL"] = "http://localhost:7000"
            
            # Set logging level based on flags (TRACE takes precedence over DEBUG)
            if trace:
                os.environ["PYTHON_LOG_LEVEL"] = "TRACE"
            elif debug:
                os.environ["PYTHON_LOG_LEVEL"] = "DEBUG"
            else:
                os.environ["PYTHON_LOG_LEVEL"] = "INFO"
                
            os.environ["HEADLESS_MODE"] = "false" if foreground else "true"
            
            print("Using local environment (URL: http://localhost:7000)")
            print("Set IFLOW_BASE_URL=http://localhost:7000")
            print(f"Set PYTHON_LOG_LEVEL={'TRACE' if trace else 'DEBUG' if debug else 'INFO'}")
            print(f"Set HEADLESS_MODE={'false (Chrome will be visible)' if foreground else 'true (Chrome will run in headless mode)'}")
        else:
            # Set up environment normally
            setup_environment(environment, foreground, debug, trace)
        
        # Set up Python path
        setup_python_path()
        
        # Run radish with all remaining arguments and get status code
        status_code = run_radish(radish_args)
        
        # Exit with the radish status code
        sys.exit(status_code)
        
    finally:
        # Clean up local server if it was started
        cleanup_local_server()

if __name__ == "__main__":
    main()
