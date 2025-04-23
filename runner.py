import sys
import os

# Add project root and core directory to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'core'))

from main import main

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python runner.py <swagger_file>")
        sys.exit(1)
    main()
