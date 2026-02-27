#!/usr/bin/env python3
"""Install pyyaml if not available."""

import subprocess
import sys

def install_pyyaml():
    """Install pyyaml using pip."""
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "pyyaml"], check=True)
        print("✅ pyyaml installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install pyyaml: {e}")
        sys.exit(1)

if __name__ == "__main__":
    install_pyyaml()