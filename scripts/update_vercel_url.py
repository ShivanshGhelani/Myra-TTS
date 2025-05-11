"""
Script to update the Vercel deployment URL in the configuration.
"""

import os
import sys
import re

# Add parent directory to path to allow imports from config package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def update_vercel_url(new_url):
    """Update the Vercel deployment URL in the deployment configuration."""
    config_file = "config/deployment.py"
    
    # Read the current file content
    with open(config_file, 'r') as file:
        content = file.read()
    
    # Replace the Vercel URL
    updated_content = re.sub(
        r'VERCEL_DEPLOYMENT_URL\s*=\s*".*?"',
        f'VERCEL_DEPLOYMENT_URL = "{new_url}"',
        content
    )
    
    # Update development flag
    updated_content = re.sub(
        r'IS_DEVELOPMENT\s*=\s*True',
        'IS_DEVELOPMENT = False',
        updated_content
    )
    
    # Write the updated content
    with open(config_file, 'w') as file:
        file.write(updated_content)
    
    print(f"Updated Vercel deployment URL to: {new_url}")
    print("Changed environment to production mode")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python scripts/update_vercel_url.py <vercel_url>")
        print("Example: python scripts/update_vercel_url.py https://myra-tts.vercel.app")
        sys.exit(1)
    
    update_vercel_url(sys.argv[1])
