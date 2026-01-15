"""
Setup verification script that checks if the environment is ready.
"""

import os
import sys
from pathlib import Path


def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✓ Python version {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor} detected. Python 3.8+ required")
        return False


def check_dependencies():
    """Check if required dependencies are installed."""
    missing = []
    
    try:
        import temporalio
        print(f"✓ temporalio {temporalio.__version__} installed")
    except ImportError:
        print("✗ temporalio not installed")
        missing.append("temporalio")
    
    try:
        import openai
        print(f"✓ openai {openai.__version__} installed")
    except ImportError:
        print("✗ openai not installed")
        missing.append("openai")
    
    try:
        import dotenv
        print("✓ python-dotenv installed")
    except ImportError:
        print("✗ python-dotenv not installed")
        missing.append("python-dotenv")
    
    return missing


def check_env_file():
    """Check if .env file exists and has required keys."""
    env_path = Path(__file__).parent / ".env"
    env_example_path = Path(__file__).parent / ".env.example"
    
    if not env_path.exists():
        print("✗ .env file not found")
        print(f"  Copy {env_example_path} to .env and fill in your values")
        return False
    
    print("✓ .env file exists")
    
    # Check if API key is set (just presence, not validity)
    with open(env_path) as f:
        content = f.read()
        if "OPENAI_API_KEY=your_openai_api_key_here" in content or "OPENAI_API_KEY=" not in content:
            print("  ⚠ OPENAI_API_KEY may not be set in .env")
            return False
    
    print("  ✓ OPENAI_API_KEY appears to be configured")
    return True


def main():
    """Run all checks."""
    print("=" * 50)
    print("Environment Setup Checker")
    print("=" * 50)
    print()
    
    print("1. Checking Python version...")
    python_ok = check_python_version()
    print()
    
    print("2. Checking dependencies...")
    missing = check_dependencies()
    print()
    
    print("3. Checking environment configuration...")
    env_ok = check_env_file()
    print()
    
    print("=" * 50)
    if python_ok and not missing and env_ok:
        print("✓ All checks passed! You're ready to run the examples.")
    else:
        print("⚠ Some setup steps are needed:")
        if not python_ok:
            print("  - Upgrade to Python 3.8 or higher")
        if missing:
            print(f"  - Install dependencies: pip install -r requirements.txt")
        if not env_ok:
            print("  - Set up your .env file with API keys")
    print()


if __name__ == "__main__":
    main()
