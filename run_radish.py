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
from pathlib import Path
from typing import List, Optional
import typer

app = typer.Typer(
    name="run_radish",
    help="Run Radish BDD tests with environment configuration",
    add_completion=False
)

# Environment URL mappings
ENVIRONMENT_URLS = {
    "dev": "http://localhost:8080",
    "qa": "http://localhost:8081", 
    "prod": "http://localhost:9000"
}

def get_script_dir() -> Path:
    """Get the directory containing this script."""
    return Path(__file__).parent.absolute()

def find_available_port(start_port: int = 7000, end_port: int = 7010) -> int:
    """Find an available port in the specified range."""
    import socket
    
    for port in range(start_port, end_port + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            continue
    
    raise RuntimeError(f"No available ports found in range {start_port}-{end_port}")

def start_local_server(port: int) -> subprocess.Popen:
    """Start a local iflow server with temporary database."""
    script_dir = get_script_dir()
    start_server_script = script_dir / "start_server.py"
    
    if not start_server_script.exists():
        raise FileNotFoundError(f"start_server.py not found at {start_server_script}")
    
    # Start the server with --init-db flag
    cmd = [sys.executable, str(start_server_script), "--port", str(port), "--init-db"]
    
    typer.echo(f"Starting local server on port {port} with temporary database...")
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Wait a bit for the server to start
    time.sleep(3)
    
    # Check if server is running
    try:
        import requests
        response = requests.get(f"http://localhost:{port}/api/artifacts", timeout=5)
        if response.status_code == 200:
            typer.echo(f"✅ Local server started successfully on port {port}")
            return process
        else:
            raise RuntimeError(f"Server responded with status {response.status_code}")
    except ImportError:
        # If requests is not available, just check if process is still running
        if process.poll() is None:
            typer.echo(f"✅ Local server started on port {port} (status check skipped)")
            return process
        else:
            raise RuntimeError("Server process failed to start")
    except Exception as e:
        raise RuntimeError(f"Failed to start local server: {e}")

def stop_local_server(process: subprocess.Popen, port: int) -> None:
    """Stop the local server and clean up."""
    if process and process.poll() is None:
        typer.echo(f"Stopping local server on port {port}...")
        process.terminate()
        try:
            process.wait(timeout=10)
            typer.echo(f"✅ Local server on port {port} stopped")
        except subprocess.TimeoutExpired:
            typer.echo(f"⚠️  Server on port {port} didn't stop gracefully, forcing...")
            process.kill()
            process.wait()
            typer.echo(f"✅ Local server on port {port} force stopped")
    else:
        typer.echo(f"Local server on port {port} is not running")

def setup_environment(environment: str, foreground: bool = False, debug: bool = False) -> None:
    """Set up environment variables for the specified environment."""
    if environment not in ENVIRONMENT_URLS:
        typer.echo(f"Error: Invalid environment '{environment}'. Must be one of: {', '.join(ENVIRONMENT_URLS.keys())}")
        raise typer.Exit(1)
    
    url = ENVIRONMENT_URLS[environment]
    os.environ["IFLOW_BASE_URL"] = url
    os.environ["PYTHON_LOG_LEVEL"] = "DEBUG" if debug else "INFO"  # Set logging level for tests
    
    # Set headless mode based on foreground flag
    if foreground:
        os.environ["HEADLESS_MODE"] = "false"  # Disable headless mode for debugging
        headless_message = "false (Chrome will be visible)"
    else:
        os.environ["HEADLESS_MODE"] = "true"  # Enable headless mode
        headless_message = "true (Chrome will run in headless mode)"
    
    typer.echo(f"Using environment: {environment} (URL: {url})")
    typer.echo(f"Set IFLOW_BASE_URL={url}")
    typer.echo(f"Set PYTHON_LOG_LEVEL={'DEBUG' if debug else 'INFO'}")
    typer.echo(f"Set HEADLESS_MODE={headless_message}")

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
    
    typer.echo(f"Running command: {' '.join(radish_cmd)}")
    
    # Run the command
    try:
        result = subprocess.run(radish_cmd, check=False)
        status_code = result.returncode
        typer.echo(f"Radish command completed with status code: {status_code}")
        return status_code
    except FileNotFoundError:
        typer.echo("Error: 'radish' command not found. Please install radish-bdd.")
        return 1

@app.command()
def main(
    environment: str = typer.Argument(
        ...,
        help="Environment to run tests against (dev, qa, prod, or 'local' for auto-started server)"
    ),
    radish_args: List[str] = typer.Argument(
        ...,
        help="Arguments to pass to radish command"
    ),
    foreground: bool = typer.Option(
        False,
        "--foreground", "-f",
        help="Run tests in foreground mode (Chrome will be visible)"
    ),
    local: bool = typer.Option(
        False,
        "--local", "-l",
        help="Automatically start a local server with temporary database and run tests against it"
    ),
    debug: bool = typer.Option(
        False,
        "--debug", "-d",
        help="Enable debug logging (sets PYTHON_LOG_LEVEL=DEBUG)"
    )
):
    """
    Run Radish BDD tests with environment configuration.
    
    The environment parameter is required and must be one of: dev, qa, prod.
    Use --local flag to automatically start a local server with temporary database.
    Use --debug flag to enable debug logging (sets PYTHON_LOG_LEVEL=DEBUG).
    
    All other arguments are passed directly to the radish command.
    
    Examples:
        run_radish.py dev tests/features/artifact_management.feature
        run_radish.py qa --tags smoke
        run_radish.py prod tests/features/ --verbose
        run_radish.py dev tests/features/test_status_filtering.feature --foreground
        run_radish.py local tests/features/ --tags @smoke --local
        run_radish.py local tests/features/test_artifact_creation.feature --local --foreground
        run_radish.py local tests/features/ --tags @smoke --local --debug
    """
    
    local_server_process = None
    local_port = None
    
    try:
        if local:
            # Override environment to 'local' when using --local flag
            environment = "local"
            
            # Find available port and start local server
            local_port = find_available_port()
            local_server_process = start_local_server(local_port)
            
            # Set up environment variables for local server
            os.environ["IFLOW_BASE_URL"] = f"http://localhost:{local_port}"
            os.environ["PYTHON_LOG_LEVEL"] = "DEBUG" if debug else "INFO"
            os.environ["HEADLESS_MODE"] = "false" if foreground else "true"
            
            typer.echo(f"Using local environment (URL: http://localhost:{local_port})")
            typer.echo(f"Set IFLOW_BASE_URL=http://localhost:{local_port}")
            typer.echo(f"Set PYTHON_LOG_LEVEL={'DEBUG' if debug else 'INFO'}")
            typer.echo(f"Set HEADLESS_MODE={'false (Chrome will be visible)' if foreground else 'true (Chrome will run in headless mode)'}")
        else:
            # Set up environment normally
            setup_environment(environment, foreground)
        
        # Set up Python path
        setup_python_path()
        
        # Run radish with all remaining arguments and get status code
        status_code = run_radish(radish_args)
        
        # Exit with the radish status code
        raise typer.Exit(status_code)
        
    finally:
        # Clean up local server if it was started
        if local_server_process and local_port:
            stop_local_server(local_server_process, local_port)

def main_simple():
    """Simple version that doesn't use typer for argument parsing."""
    if len(sys.argv) < 3:
        print("Usage: run_radish.py <environment> <radish_args...> [--foreground] [--local] [--debug]")
        print("Example: run_radish.py dev tests/features/ --tags @smoke")
        print("Example: run_radish.py dev tests/features/test_status_filtering.feature --foreground")
        print("Example: run_radish.py local tests/features/ --tags @smoke --local")
        print("Example: run_radish.py local tests/features/test_artifact_creation.feature --local --foreground")
        print("Example: run_radish.py local tests/features/ --tags @smoke --local --debug")
        sys.exit(1)
    
    environment = sys.argv[1]
    radish_args = sys.argv[2:]
    
    # Check for flags
    foreground = False
    local = False
    debug = False
    
    if "--foreground" in radish_args:
        foreground = True
        radish_args.remove("--foreground")
    
    if "--local" in radish_args:
        local = True
        radish_args.remove("--local")
    
    if "--debug" in radish_args:
        debug = True
        radish_args.remove("--debug")
    
    local_server_process = None
    local_port = None
    
    def cleanup_local_server(signum=None, frame=None):
        """Clean up local server on signal or exit."""
        if local_server_process and local_port:
            stop_local_server(local_server_process, local_port)
        if signum:
            sys.exit(1)
    
    try:
        if local:
            # Override environment to 'local' when using --local flag
            environment = "local"
            
            # Find available port and start local server
            local_port = find_available_port()
            local_server_process = start_local_server(local_port)
            
            # Set up signal handlers for cleanup
            signal.signal(signal.SIGINT, cleanup_local_server)
            signal.signal(signal.SIGTERM, cleanup_local_server)
            atexit.register(cleanup_local_server)
            
            # Set up environment variables for local server
            os.environ["IFLOW_BASE_URL"] = f"http://localhost:{local_port}"
            os.environ["PYTHON_LOG_LEVEL"] = "DEBUG" if debug else "INFO"
            os.environ["HEADLESS_MODE"] = "false" if foreground else "true"
            
            print(f"Using local environment (URL: http://localhost:{local_port})")
            print(f"Set IFLOW_BASE_URL=http://localhost:{local_port}")
            print(f"Set PYTHON_LOG_LEVEL={'DEBUG' if debug else 'INFO'}")
            print(f"Set HEADLESS_MODE={'false (Chrome will be visible)' if foreground else 'true (Chrome will run in headless mode)'}")
        else:
            # Set up environment normally
            setup_environment(environment, foreground)
        
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
    main_simple()
