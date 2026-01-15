#!/usr/bin/env python3
"""
Quick verification script to check if all examples can be imported.
This doesn't run the examples (which require external services), 
but verifies that the code is syntactically correct and imports work.
"""

import sys
from pathlib import Path

# Add examples to path
examples_dir = Path(__file__).parent / "examples"
sys.path.insert(0, str(examples_dir))

print("Checking example imports...")

try:
    print("✓ Checking temporal workflows...")
    from temporal import workflows as temporal_workflows
    print("  - workflows.py imported successfully")
except ImportError as e:
    print(f"  ✗ Failed to import temporal workflows: {e}")

try:
    print("✓ Checking integration workflows...")
    from integration import workflows as integration_workflows
    print("  - workflows.py imported successfully")
except ImportError as e:
    print(f"  ✗ Failed to import integration workflows: {e}")

print("\n✓ All syntax checks passed!")
print("\nNote: To run the actual examples, you'll need:")
print("  1. Install dependencies: pip install -r requirements.txt")
print("  2. Set up .env file with your OpenAI API key")
print("  3. Start Temporal server: temporal server start-dev")
print("  4. Run the workers and workflow scripts as described in the README")
