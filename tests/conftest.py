"""Test configuration for pytest."""

import sys
from pathlib import Path

# Add the examples directory to the path
examples_dir = Path(__file__).parent.parent / "examples"
sys.path.insert(0, str(examples_dir))
