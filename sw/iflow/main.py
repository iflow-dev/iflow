#!/usr/bin/env python3
"""
Main entry point for the iflow application.
"""

import sys
import argparse
from pathlib import Path
from .app import IFlowApp


def main():
    """Main entry point for the iflow application."""
    parser = argparse.ArgumentParser(
        description="iflow - Project Artifact Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  iflow                    # Run with default database path (.iflow)
  iflow --database ./my-project  # Run with custom database path
  iflow --help            # Show this help message
        """
    )
    
    parser.add_argument(
        '--database', '-d',
        default='.iflow',
        help='Path to the git database (default: .iflow)'
    )
    
    parser.add_argument(
        '--version', '-v',
        action='version',
        version='iflow 0.3.0'
    )
    
    args = parser.parse_args()
    
    try:
        # Create and run the application
        app = IFlowApp(database_path=args.database)
        print(f"Starting iflow with database: {args.database}")
        print("Press Ctrl+C to exit")
        app.run()
        
    except KeyboardInterrupt:
        print("\nExiting iflow...")
        sys.exit(0)
    except Exception as e:
        print(f"Error starting iflow: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
