#!/usr/bin/env python3
"""Initialize skills development environment."""

import os
import subprocess
import sys
from pathlib import Path

def install_dependencies():
    """Install required dependencies."""
    print("📦 Installing dependencies...")
    
    # Install pyyaml if not available
    try:
        import yaml
        print("✅ pyyaml already available")
    except ImportError:
        print("📦 Installing pyyaml...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyyaml"], check=True)
        print("✅ pyyaml installed successfully")

def main():
    """Main initialization function."""
    print("🔧 Setting up Agent Skills development environment...")
    
    # Create virtual environment if it doesn't exist
    venv_dir = Path("venv_env")
    if not venv_dir.exists():
        print("📦 Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", "venv_env"], check=True)
        print("✅ Virtual environment created")
    
    # Install dependencies
    install_dependencies()
    
    # Copy .opencode and .claude directories for easy access
    print("📁 Setting up local skill directories...")
    for dir_name in [".opencode/skills", ".claude/skills"]:
        target_dir = Path(dir_name)
        target_dir.mkdir(exist_ok=True)
        print(f"✅ Created {dir_name} directory")
    
    print("✅ Skills environment setup complete!")
    print("\n🚀 You can now start creating and validating Agent Skills!")
    print("\n💡 Quick start:")
    print("  Create a skill: python3 tools.py create-skill <name> <description>")
    print("  Validate skills: python3 tools.py validate")
    print("  Copy skills: python3 tools.py copy-skills")
    print("  Update AGENTS.md: python3 tools.py update-agents")

if __name__ == "__main__":
    main()