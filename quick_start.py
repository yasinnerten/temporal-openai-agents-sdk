#!/usr/bin/env python3
"""Quick start for Agent Skills development."""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Setup development environment and tools."""
    print("🚀 Agent Skills Quick Start")
    print("=" * 50)
    print("Welcome to Agent Skills development!")
    print("")
    
    # Check Python
    if not os.system("python3 --version 2>/dev/null"):
        print("❌ Python 3 is not installed")
        print("Please install Python 3.8+ to continue.")
        sys.exit(1)
    
    print("✅ Python 3 detected")
    print("")
    
    # Check if venv exists
    if not Path("venv").exists():
        print("📦 Creating virtual environment...")
        os.system("python3 -m venv venv")
        print("✅ Virtual environment created")
    else:
        print("📁 Virtual environment already exists")
    
    print("📦 Installing dependencies...")
    # Install pyyaml using pip in venv
    subprocess.run(["venv/bin/pip", "install", "pyyaml"], check=True)
    
    print("✅ Dependencies installed")
    print("")
    
    # Check if we're in the skills directory
    if not Path("skills").exists():
        print("📁 Creating skills directory...")
        os.makedirs("skills")
        print("✅ Skills directory created")
    
    print("🎯 Next steps:")
    print("1. Create your first skill:")
    print("   python3 create_simple_skill.py my-agent 'My AI agent for X task'")
    print("")
    print("2. List available skills:")
    print("   python3 tools.py list")
    print("")
    print("3. Validate all skills:")
    print("   python3 validate_skills")
    print("")
    print("4. Copy skills to platform:")
    print("   python3 tools.py copy-skills")
    print("")
    print("5. For help:")
    print("   python3 tools.py")

if __name__ == "__main__":
    main()