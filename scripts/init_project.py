"""
Initialize MyraTTS project for development.
"""

import os
import sys
import subprocess

# Add parent directory to path to allow imports from project modules if needed
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def check_python_version():
    """Check if Python version is compatible."""
    required_version = (3, 9)
    current_version = sys.version_info
    
    if current_version < required_version:
        print(f"Error: Python {required_version[0]}.{required_version[1]} or higher is required.")
        print(f"Current version: {current_version[0]}.{current_version[1]}")
        sys.exit(1)

def create_virtual_env():
    """Create a virtual environment if it doesn't exist."""
    if not os.path.exists("myra_tts"):
        print("Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", "myra_tts"], check=True)
        print("Virtual environment created successfully!")
    else:
        print("Virtual environment already exists.")

def install_dependencies():
    """Install dependencies from requirements.txt."""
    if os.name == 'nt':  # Windows
        pip_path = os.path.join("myra_tts", "Scripts", "pip")
    else:  # Unix/Linux/Mac
        pip_path = os.path.join("myra_tts", "bin", "pip")
    
    print("Installing dependencies...")
    subprocess.run([pip_path, "install", "-r", "requirements.txt"], check=True)
    print("Dependencies installed successfully!")

def create_directories():
    """Create necessary directories if they don't exist."""
    directories = ["audio", "audio/samples", "static/audio"]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Directory '{directory}' created or verified.")

def main():
    """Main initialization function."""
    print("Initializing MyraTTS project...")
    
    check_python_version()
    create_virtual_env()
    install_dependencies()
    create_directories()
    
    print("\nProject initialized successfully!")
    print("\nTo activate the virtual environment:")
    if os.name == 'nt':  # Windows
        print("myra_tts\\Scripts\\activate")
    else:  # Unix/Linux/Mac
        print("source myra_tts/bin/activate")
    
    print("\nTo run the application:")
    print("uvicorn api.main:create_app --reload")
    print("\nThe application will be available at: http://127.0.0.1:8000/")

if __name__ == "__main__":
    main()
