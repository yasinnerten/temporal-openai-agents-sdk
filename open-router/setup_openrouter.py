"""
Setup script for OpenRouter integration.
Checks if OpenRouter API key is configured and validates the setup.
Includes venv management and automated key retrieval.
"""

import os
import sys
import subprocess
from pathlib import Path


def setup_venv():
    """Create and activate virtual environment."""
    venv_path = Path(__file__).parent / "venv"
    
    if venv_path.exists():
        print("✓ Virtual environment already exists")
        return True
    
    print("Creating virtual environment...")
    try:
        subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)
        print("✓ Virtual environment created")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to create venv: {e}")
        return False


def get_venv_python():
    """Get path to python in venv."""
    venv_path = Path(__file__).parent / "venv"
    python_path = venv_path / "bin" / "python"
    
    if not python_path.exists():
        python_path = venv_path / "Scripts" / "python.exe"
    
    return python_path if python_path.exists() else sys.executable


def install_dependencies():
    """Install required dependencies in venv."""
    python_path = get_venv_python()
    required = ["openai", "python-dotenv", "temporalio", "requests"]
    
    print("Installing dependencies...")
    for package in required:
        try:
            subprocess.run(
                [str(python_path), "-m", "pip", "install", "-q", package],
                check=True,
                capture_output=True
            )
            print(f"✓ {package} installed")
        except subprocess.CalledProcessError:
            print(f"✗ Failed to install {package}")
            return False
    
    # Try to install agents with compatible tensorflow version
    print("Installing agents with TensorFlow 1.x compatibility...")
    try:
        subprocess.run(
            [str(python_path), "-m", "pip", "install", "-q", "tensorflow==1.15.0", "agents"],
            check=True,
            capture_output=True
        )
        print(f"✓ agents installed with TensorFlow 1.15.0")
    except subprocess.CalledProcessError:
        print(f"⚠ agents installation failed")
        print(f"  TensorFlow compatibility issue detected")
        print(f"  Proceeding without agents (optional dependency)")
        print(f"  You can still use OpenRouter without agent features")
    
    return True


def fetch_api_key_interactive():
    """Interactively get API key from user."""
    print("\n" + "=" * 50)
    print("OpenRouter API Key Setup")
    print("=" * 50)
    print("\nTo get your API key:")
    print("1. Visit: https://openrouter.ai/keys")
    print("2. Sign up for a free account")
    print("3. Copy your API key (starts with 'sk-or-v1-')")
    print()
    
    api_key = input("Paste your OpenRouter API key: ").strip()
    
    if not api_key.startswith("sk-or-v1-"):
        print("⚠ Warning: Key doesn't match expected format (sk-or-v1-*)")
        confirm = input("Continue anyway? (y/n): ").strip().lower()
        if confirm != 'y':
            return None
    
    return api_key


def validate_api_key(api_key):
    """Validate API key by making a test request."""
    python_path = get_venv_python()
    
    test_script = '''
import sys
try:
    from openai import OpenAI
    api_key = sys.argv[1]
    client = OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")
    response = client.models.list()
    print("valid")
except Exception as e:
    print(f"invalid")
'''
    
    try:
        result = subprocess.run(
            [str(python_path), "-c", test_script, api_key],
            capture_output=True,
            text=True,
            timeout=10
        )
        return "valid" in result.stdout
    except Exception:
        return False


def check_openrouter_env():
    """Check if .env file exists and has OpenRouter API key."""
    env_path = Path(__file__).parent / ".env"
    env_example_path = Path(__file__).parent / ".env.example"
    
    if not env_path.exists():
        print("✗ .env file not found in open-router/ folder")
        
        api_key = fetch_api_key_interactive()
        if not api_key:
            print("  Setup cancelled")
            return False
        
        print("\nValidating API key...")
        if validate_api_key(api_key):
            print("✓ API key is valid")
            with open(env_path, 'w') as f:
                f.write(f"OPENROUTER_API_KEY={api_key}\n")
            print(f"✓ .env file created with API key")
            return True
        else:
            print("✗ API key validation failed. Please check your key.")
            return False
    
    print("✓ .env file exists")
    
    with open(env_path) as f:
        content = f.read()
        if "OPENROUTER_API_KEY=sk-or-v1-your-api-key-here" in content or "OPENROUTER_API_KEY=" not in content:
            print("  ⚠ OPENROUTER_API_KEY not set or is placeholder")
            return False
    
    print("  ✓ OPENROUTER_API_KEY appears to be configured")
    return True


def check_dependencies():
    """Check if OpenRouter dependencies are installed."""
    python_path = get_venv_python()
    required = ["openai", "dotenv", "temporalio"]
    optional = ["agents"]
    missing = []
    
    for package in required:
        try:
            subprocess.run(
                [str(python_path), "-c", f"import {package.replace('-', '_')}"],
                capture_output=True,
                check=True
            )
            print(f"✓ {package} installed")
        except subprocess.CalledProcessError:
            print(f"✗ {package} not installed")
            missing.append(package)
    
    # Check optional dependencies
    for package in optional:
        try:
            subprocess.run(
                [str(python_path), "-c", f"import {package.replace('-', '_')}"],
                capture_output=True,
                check=True
            )
            print(f"✓ {package} installed")
        except subprocess.CalledProcessError:
            print(f"⚠ {package} not installed (required for agent features)")
    
    return missing


def main():
    """Run setup checks for OpenRouter."""
    print("=" * 50)
    print("OpenRouter Setup Checker")
    print("=" * 50)
    print()
    
    print("1. Setting up virtual environment...")
    if not setup_venv():
        return False
    print()
    
    print("2. Installing dependencies...")
    if not install_dependencies():
        return False
    print()
    
    print("3. Checking OpenRouter configuration...")
    env_ok = check_openrouter_env()
    print()
    
    print("4. Verifying dependencies...")
    missing = check_dependencies()
    print()
    
    print("=" * 50)
    if not missing and env_ok:
        print("✓ OpenRouter setup is complete!")
        print("  To activate venv and run example:")
        print("  source venv/bin/activate")
        print("  python example.py")
    else:
        print("⚠ Setup incomplete")
    print()
    
    return env_ok and not missing


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)