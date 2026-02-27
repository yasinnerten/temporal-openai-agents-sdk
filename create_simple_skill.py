#!/usr/bin/env python3
"""Create new Agent Skills."""

import os
import re
import sys
from pathlib import Path
import yaml

def create_skill(skill_dir: Path, name: str, description: str):
    """Create a new skill."""
    # Validate name
    if len(name) < 1 or len(name) > 64:
        print(f"❌ Invalid name: must be 1-64 characters")
        return
    
    if not re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', name):
        print(f"❌ Invalid name: lowercase alphanumeric with hyphens only")
        return
    
    if name.startswith('-') or name.endswith('-'):
        print("❌ Invalid name: cannot start or end with hyphen")
        return
    
    # Validate description
    if len(description) < 1 or len(description) > 1024:
        print("❌ Invalid description: must be 1-1024 characters")
        return
    
    # Create skill directory
    skill_path = skill_dir / name
    os.makedirs(skill_path, exist_ok=True)
    
    # Create SKILL.md
    skill_content = f"""---
name: {name}
description: {description}
license: Apache-2.0
metadata:
  category: development
  tags: [agent, tools]
---

# {name}

This skill provides {description}.

## Usage

Use the `/skill` command in OpenCode or Cursor to load this skill.

## Examples

```python
# Example code here
```
"""
    
    with open(skill_path / "SKILL.md", 'w') as f:
        f.write(skill_content)
    
    print(f"✅ Created skill: {name}")
    print(f"📍 Location: {skill_path}")

def main():
    """Main function."""
    if len(sys.argv) < 3:
        print("Usage: python create_simple_skill.py <name> <description>")
        print("Example: python create_simple_skill.py web-searcher 'Search the web for information'")
        return
    
    name = sys.argv[1]
    description = sys.argv[2]
    
    # Create in skills directory
    skills_dir = Path("skills")
    create_skill(skills_dir, name, description)

if __name__ == "__main__":
    main()