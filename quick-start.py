#!/usr/bin/env python3
"""
Quick start script for the Intelligent Document Redaction Tool.
This installs minimal dependencies to get you started quickly.
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


def main():
    """Quick setup with minimal dependencies."""
    print("🚀 Quick Start - Intelligent Document Redaction Tool")
    print("=" * 55)
    print("This will install minimal dependencies for a quick demo.")
    print("For full features, run 'python setup.py' later.")
    print()

    # Create .env file
    env_example = Path(".env.example")
    env_file = Path(".env")

    if env_example.exists() and not env_file.exists():
        try:
            with open(env_example, 'r') as src, open(env_file, 'w') as dst:
                dst.write(src.read())
            print("✅ Created .env file")
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")

    # Create directories
    for directory in ["uploads", "outputs"]:
        Path(directory).mkdir(exist_ok=True)
    print("✅ Created directories")

    # Install minimal requirements
    minimal_req = Path("backend/requirements-minimal.txt")
    if minimal_req.exists():
        success = run_command(
            f"pip install -r {minimal_req}",
            "Installing minimal Python dependencies"
        )
        if not success:
            print("❌ Failed to install dependencies")
            return

    # Download spaCy model
    print("\n🔄 Downloading spaCy model (this may take a moment)...")
    if run_command("python -m spacy download en_core_web_sm", "Downloading spaCy model"):
        print("✅ spaCy model downloaded")
    else:
        print("⚠️  spaCy model download failed - some features may not work")

    print("\n" + "=" * 55)
    print("🎉 Quick setup completed!")
    print("\n📋 Next steps:")
    print("1. Start the backend:")
    print("   cd backend")
    print("   python -m uvicorn app.main:app --reload")
    print("\n2. Open http://localhost:8000/api/docs in your browser")
    print("3. Test the API endpoints")
    print("\n💡 For the full UI, install Node.js and run:")
    print("   cd frontend && npm install && npm run dev")
    print("\n📖 For complete setup, run: python setup.py")


if __name__ == "__main__":
    main()
