"""
Script to update the GitHub repository URL in the configuration.
"""

import os
import sys
import re

# Add parent directory to path to allow imports from config package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def update_repository_url(new_url):
    """Update the GitHub repository URL in the deployment configuration."""
    config_file = "config/deployment.py"
    
    # Read the current file content
    with open(config_file, 'r') as file:
        content = file.read()
    
    # Replace the repository URL
    updated_content = re.sub(
        r'GITHUB_REPOSITORY_URL\s*=\s*".*?"',
        f'GITHUB_REPOSITORY_URL = "{new_url}"',
        content
    )
    
    # Write the updated content
    with open(config_file, 'w') as file:
        file.write(updated_content)
    
    print(f"Updated GitHub repository URL to: {new_url}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python scripts/update_repo_url.py <repository_url>")
        print("Example: python scripts/update_repo_url.py https://github.com/username/MyraTTS")
        sys.exit(1)
    
    update_repository_url(sys.argv[1])
