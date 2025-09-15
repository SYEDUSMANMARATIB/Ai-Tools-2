#!/usr/bin/env python3
"""
Setup script for the Intelligent Document Redaction Tool.
This script helps with initial setup and model downloads.
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False


def check_python_version():
    """Check if Python version is compatible."""
    print("🔍 Checking Python version...")
    if sys.version_info < (3, 9):
        print("❌ Python 3.9 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} is compatible")
    return True


def install_backend_dependencies():
    """Install backend Python dependencies."""
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ Backend directory not found")
        return False

    requirements_file = backend_dir / "requirements.txt"
    if not requirements_file.exists():
        print("❌ requirements.txt not found in backend directory")
        return False

    # Install requirements
    return run_command(
        f"pip install -r {requirements_file}",
        "Installing Python dependencies"
    )


def download_spacy_model():
    """Download spaCy English model."""
    return run_command(
        "python -m spacy download en_core_web_sm",
        "Downloading spaCy English model"
    )


def install_frontend_dependencies():
    """Install frontend Node.js dependencies."""
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return False

    package_json = frontend_dir / "package.json"
    if not package_json.exists():
        print("❌ package.json not found in frontend directory")
        return False

    # Change to frontend directory and install
    original_dir = os.getcwd()
    try:
        os.chdir(frontend_dir)
        success = run_command("npm install", "Installing Node.js dependencies")
        return success
    finally:
        os.chdir(original_dir)


def create_env_file():
    """Create .env file from template."""
    env_example = Path(".env.example")
    env_file = Path(".env")

    if not env_example.exists():
        print("❌ .env.example file not found")
        return False

    if env_file.exists():
        print("⚠️  .env file already exists, skipping creation")
        return True

    try:
        with open(env_example, 'r') as src, open(env_file, 'w') as dst:
            content = src.read()
            # Set local models to true by default
            content = content.replace('USE_LOCAL_MODELS=true', 'USE_LOCAL_MODELS=true')
            dst.write(content)
        print("✅ Created .env file from template")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False


def create_directories():
    """Create necessary directories."""
    directories = ["uploads", "outputs", "models"]

    for directory in directories:
        dir_path = Path(directory)
        if not dir_path.exists():
            try:
                dir_path.mkdir(parents=True, exist_ok=True)
                print(f"✅ Created directory: {directory}")
            except Exception as e:
                print(f"❌ Failed to create directory {directory}: {e}")
                return False

    return True


def main():
    """Main setup function."""
    print("🚀 Setting up Intelligent Document Redaction Tool")
    print("=" * 50)

    # Check Python version
    if not check_python_version():
        sys.exit(1)

    # Create necessary directories
    if not create_directories():
        print("❌ Failed to create directories")
        sys.exit(1)

    # Create .env file
    if not create_env_file():
        print("❌ Failed to create .env file")
        sys.exit(1)

    # Install backend dependencies
    if not install_backend_dependencies():
        print("❌ Failed to install backend dependencies")
        sys.exit(1)

    # Download spaCy model
    if not download_spacy_model():
        print("⚠️  Failed to download spaCy model - you can install it manually later")
        print("   Run: python -m spacy download en_core_web_sm")

    # Install frontend dependencies (optional)
    print("\n🔄 Installing frontend dependencies...")
    if not install_frontend_dependencies():
        print("⚠️  Failed to install frontend dependencies")
        print("   You can install them manually by running 'npm install' in the frontend directory")

    print("\n" + "=" * 50)
    print("🎉 Setup completed!")
    print("\n📋 Next steps:")
    print("1. Edit the .env file and add your API keys (optional)")
    print("2. Start the backend: cd backend && uvicorn app.main:app --reload")
    print("3. Start the frontend: cd frontend && npm run dev")
    print("4. Open http://localhost:3000 in your browser")
    print("\n📖 For detailed instructions, see INSTALLATION.md")


if __name__ == "__main__":
    main()
