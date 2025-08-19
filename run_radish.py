#!/usr/bin/env python3
"""
Radish test runner with environment support.

This script provides a convenient way to run Radish BDD tests with automatic
environment configuration and Python path setup.
"""

import os
import sys
import subprocess
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

def setup_environment(environment: str) -> None:
    """Set up environment variables for the specified environment."""
    if environment not in ENVIRONMENT_URLS:
        typer.echo(f"Error: Invalid environment '{environment}'. Must be one of: {', '.join(ENVIRONMENT_URLS.keys())}")
        raise typer.Exit(1)
    
    url = ENVIRONMENT_URLS[environment]
    os.environ["IFLOW_BASE_URL"] = url
    typer.echo(f"Using environment: {environment} (URL: {url})")

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

def run_radish(args: List[str]) -> None:
    """Run the radish command with the given arguments."""
    script_dir = get_script_dir()
    tests_dir = script_dir / "tests"
    
    # Check if --basedir or -b is already provided
    has_basedir = any(arg in ["--basedir", "-b"] for arg in args)
    
    # Build the radish command
    radish_cmd = ["radish"] + args
    if not has_basedir:
        radish_cmd.extend(["-b", str(tests_dir)])
    
    # Run the command
    try:
        subprocess.run(radish_cmd, check=True)
    except subprocess.CalledProcessError as e:
        raise typer.Exit(e.returncode)
    except FileNotFoundError:
        typer.echo("Error: 'radish' command not found. Please install radish-bdd.")
        raise typer.Exit(1)

@app.command()
def main(
    environment: str = typer.Argument(
        ...,
        help="Environment to run tests against (dev, qa, prod)"
    ),
    radish_args: List[str] = typer.Argument(
        ...,
        help="Arguments to pass to radish command"
    )
):
    """
    Run Radish BDD tests with environment configuration.
    
    The environment parameter is required and must be one of: dev, qa, prod.
    
    All other arguments are passed directly to the radish command.
    
    Examples:
        run_radish.py dev tests/features/artifact_management.feature
        run_radish.py qa --tags smoke
        run_radish.py prod tests/features/ --verbose
    """
    # Set up environment
    setup_environment(environment)
    
    # Set up Python path
    setup_python_path()
    
    # Run radish with all remaining arguments
    run_radish(radish_args)

def main_simple():
    """Simple version that doesn't use typer for argument parsing."""
    if len(sys.argv) < 3:
        print("Usage: run_radish.py <environment> <radish_args...>")
        print("Example: run_radish.py dev tests/features/ --tags @smoke")
        sys.exit(1)
    
    environment = sys.argv[1]
    radish_args = sys.argv[2:]
    
    # Set up environment
    setup_environment(environment)
    
    # Set up Python path
    setup_python_path()
    
    # Run radish with all remaining arguments
    run_radish(radish_args)

if __name__ == "__main__":
    main_simple()
