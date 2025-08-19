#!/usr/bin/env python3
"""
Generic Server Management Script for iflow Environments
Usage: /opt/iflow/<env>/server {start|stop|status|restart}
"""

import os
import sys
import time
import signal
import subprocess
import yaml
import argparse
from pathlib import Path
from typing import Optional, Dict, Any

# Colors for output
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    NC = '\033[0m'  # No Color

class ServerManager:
    def __init__(self, env_path: str):
        self.env_path = Path(env_path)
        self.config = self._load_config()
        self.pid_file = f"/tmp/iflow-{self.config['name']}.pid"
        
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from .server.yaml file"""
        config_file = self.env_path / ".server.yaml"
        if not config_file.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_file}")
        
        with open(config_file, 'r') as f:
            return yaml.safe_load(f)
    
    def is_running(self) -> bool:
        """Check if server is running"""
        if not os.path.exists(self.pid_file):
            return False
        
        try:
            with open(self.pid_file, 'r') as f:
                pid = int(f.read().strip())
            
            # Check if process exists
            os.kill(pid, 0)
            return True
        except (ValueError, OSError):
            # Remove invalid PID file
            if os.path.exists(self.pid_file):
                os.remove(self.pid_file)
            return False
    
    def get_status(self) -> bool:
        """Get server status"""
        if not self.is_running():
            print(f"{Colors.RED}Server is not running{Colors.NC}")
            return False
        
        try:
            with open(self.pid_file, 'r') as f:
                pid = int(f.read().strip())
            
            # Check if port is listening
            port = self.config['port']
            result = subprocess.run(['lsof', '-ti', f':{port}'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0 and str(pid) in result.stdout:
                print(f"{Colors.GREEN}Server is running (PID: {pid}, Port: {port}){Colors.NC}")
                return True
            else:
                print(f"{Colors.YELLOW}Server process exists but port {port} is not listening{Colors.NC}")
                return False
        except Exception as e:
            print(f"{Colors.RED}Error checking status: {e}{Colors.NC}")
            return False
    
    def start_server(self) -> bool:
        """Start the server"""
        if self.is_running():
            print(f"{Colors.RED}Server is already running{Colors.NC}")
            self.get_status()
            return False
        
        print(f"Starting iflow {self.config['name'].title()} Environment...")
        
        # Change to environment directory
        os.chdir(self.env_path)
        
        # Check/create virtual environment
        venv_path = self.env_path / "venv"
        if not venv_path.exists():
            print("Creating virtual environment...")
            subprocess.run(['python3', '-m', 'venv', 'venv'], check=True)
        
        # Activate virtual environment and install package
        if sys.platform == "win32":
            activate_script = venv_path / "Scripts" / "activate"
            pip_path = venv_path / "Scripts" / "pip"
        else:
            activate_script = venv_path / "bin" / "activate"
            pip_path = venv_path / "bin" / "pip"
        
        # Install iflow package if needed
        try:
            result = subprocess.run([str(pip_path), 'show', 'iflow'], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                print("Installing iflow package...")
                subprocess.run([str(pip_path), 'install', '/Users/claudio/realtime/reos2'], 
                             check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error installing package: {e}")
            return False
        
        # Setup database if needed
        db_path = self.env_path / self.config['database']
        if not db_path.exists():
            print(f"Setting up {self.config['database']} database...")
            subprocess.run(['git', 'clone', self.config['database_url'], str(db_path)], 
                         check=True)
        
        # Start web server
        print(f"Starting web server on port {self.config['port']}...")
        
        # Build command
        cmd = [
            str(venv_path / "bin" / "python"), '-m', 'iflow.web_server',
            '--port', str(self.config['port']),
            '--database', str(db_path),
            '--host', '0.0.0.0',
            '--title', f"iflow - {self.config['name'].title()} Environment"
        ]
        
        # Start in background
        try:
            process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, 
                                     stderr=subprocess.DEVNULL)
            
            # Save PID
            with open(self.pid_file, 'w') as f:
                f.write(str(process.pid))
            
            # Wait and check status
            time.sleep(2)
            if self.is_running():
                print(f"{Colors.GREEN}Server started successfully{Colors.NC}")
                self.get_status()
                return True
            else:
                print(f"{Colors.RED}Failed to start server{Colors.NC}")
                if os.path.exists(self.pid_file):
                    os.remove(self.pid_file)
                return False
                
        except Exception as e:
            print(f"{Colors.RED}Error starting server: {e}{Colors.NC}")
            return False
    
    def stop_server(self) -> bool:
        """Stop the server"""
        if not self.is_running():
            print(f"{Colors.YELLOW}Server is not running{Colors.NC}")
            return True
        
        try:
            with open(self.pid_file, 'r') as f:
                pid = int(f.read().strip())
            
            print(f"Stopping server (PID: {pid})...")
            
            # Try graceful shutdown
            os.kill(pid, signal.SIGTERM)
            
            # Wait for graceful shutdown
            for i in range(10):
                if not self.is_running():
                    break
                time.sleep(1)
            
            # Force kill if still running
            if self.is_running():
                print("Force killing server...")
                os.kill(pid, signal.SIGKILL)
                time.sleep(1)
            
            # Remove PID file
            if os.path.exists(self.pid_file):
                os.remove(self.pid_file)
            
            print(f"{Colors.GREEN}Server stopped{Colors.NC}")
            return True
            
        except Exception as e:
            print(f"{Colors.RED}Error stopping server: {e}{Colors.NC}")
            return False
    
    def restart_server(self) -> bool:
        """Restart the server"""
        print("Restarting server...")
        if self.stop_server():
            time.sleep(2)
            return self.start_server()
        return False

def main():
    parser = argparse.ArgumentParser(description='iflow Server Management')
    parser.add_argument('command', choices=['start', 'stop', 'status', 'restart'],
                       help='Server command to execute')
    parser.add_argument('--env', required=True, help='Environment path')
    
    args = parser.parse_args()
    
    try:
        manager = ServerManager(args.env)
        
        if args.command == 'start':
            success = manager.start_server()
            sys.exit(0 if success else 1)
        elif args.command == 'stop':
            success = manager.stop_server()
            sys.exit(0 if success else 1)
        elif args.command == 'status':
            success = manager.get_status()
            sys.exit(0 if success else 1)
        elif args.command == 'restart':
            success = manager.restart_server()
            sys.exit(0 if success else 1)
            
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.NC}")
        sys.exit(1)

if __name__ == '__main__':
    main()
