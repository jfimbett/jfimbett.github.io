#!/usr/bin/env python3
"""
Build script for the academic website.
Fetches paper data and builds the website.
"""

import os
import subprocess
import sys

def main():
    """Main function to build the website."""
    # Define the project root directory
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Print current working directory
    print(f"Working directory: {os.getcwd()}")
    print(f"Project root: {project_root}")
    
    # Run the SSRN fetcher script
    print("Fetching papers from SSRN...")
    try:
        script_path = os.path.join(project_root, 'scripts', 'fetch_ssrn_data.py')
        subprocess.run([sys.executable, script_path], check=True)
        print("Papers fetched successfully!")
    except subprocess.CalledProcessError:
        print("Error: Failed to fetch papers from SSRN.", file=sys.stderr)
        return 1
    
    print("Website is ready to be deployed.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
