#!/usr/bin/env python3
"""Skill Creator Tool - Create new Agent Skills easily."""

import os
import re
import yaml
from pathlib import Path

def validate_skill_name(name: str) -> tuple[bool, str]:
    """Validate skill name according to Agent Skills specification."""
    if len(name) < 1 or len(name) > 64:
        return False, "Name must be 1-64 characters"
    
    if not re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', name):
        return False, "Name must be lowercase alphanumeric with hyphen separators"
    
    if name.startswith('-') or name.endswith('-'):
        return False, "Name cannot start or end with hyphen"
    
    return True, "Valid"

def validate_description(desc: str) -> tuple[bool, str]:
    """Validate skill description."""
    if len(desc) < 1 or len(desc) > 1024:
        return False, "Description must be 1-1024 characters"
    
    return True, "Valid"

def get_skill_templates() -> dict:
    """Get available skill templates."""
    return {
        "1": {
            "name": "basic-agent",
            "description": "Basic AI agent with tool calling capabilities",
            "content": """---
name: basic-agent
description: Basic AI agent with tool calling capabilities
license: Apache-2.0
metadata:
  category: agents
  tags: [ai, agent, python]
---

# Basic Agent

This skill provides a simple AI agent that can use tools and execute tasks.

## Setup
```python
from openai import AsyncOpenAI

class BasicAgent:
    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key)
        self.tools = {
            "search": self.search_web,
            "calculate": self.calculate,
        }
```
"""
        },
        "2": {
            "name": "web-scraper",
            "description": "Web scraping agent with HTML parsing",
            "content": """---
name: web-scraper
description: Web scraping agent with HTML parsing
license: Apache-2.0
---
"""
        }
    }

def create_skill_folder(skill_dir: Path, skill_name: str, description: str, template: str) -> Path:
    """Create skill folder with SKILL.md file."""
    skill_path = skill_dir / skill_name
    os.makedirs(skill_path, exist_ok=True)
    
    skill_content = template.format(
        name=skill_name,
        description=description
    )
    
    skill_file = skill_path / "SKILL.md"
    with open(skill_file, 'w') as f:
        f.write(skill_content)
    
    print(f"✅ Created skill: {skill_name}")
    print(f"📍 Location: {skill_file}")
    
    # Create optional directories
    scripts_dir = skill_path / "scripts"
    scripts_dir.mkdir(exist_ok=True)
    (scripts_dir / "setup.sh").touch()
    
    references_dir = skill_path / "references"
    references_dir.mkdir(exist_ok=True)
    
    return skill_file

def list_skills(skills_dir: Path) -> None:
    """List available skills."""
    if not skills_dir.exists():
        print("❌ Skills directory not found")
        return
    
    skill_dirs = [d for d in skills_dir.iterdir() if d.is_dir()]
    
    if not skill_dirs:
        print("No skills found. Use 'create' command to create one.")
        return
    
    print("Available skills:")
    for i, skill_dir in enumerate(skill_dirs, 1):
        skill_file = skill_dir / "SKILL.md"
        if skill_file.exists():
            try:
                with open(skill_file, 'r') as f:
                    content = f.read()
                    if '---' in content:
                        frontmatter = content.split('---')[1] if '---' in content else ''
                        data = yaml.safe_load(frontmatter)
                        name = data.get('name', 'unknown')
                        desc = data.get('description', 'No description')
                        print(f"  {i}. {name} - {desc}")
            except Exception as e:
                print(f"  {i}. Error reading SKILL.md: {e}")

def main():
    """Main CLI interface."""
    import sys
    
    skills_dir = Path("skills")
    
    if len(sys.argv) < 2:
        print("Usage: python create_skill.py <command>")
        print("Commands:")
        print("  list - List available skills")
        print("  create <name> <description> - Create new skill")
        print("  validate - Validate all skills")
        return
    
    command = sys.argv[1]
    
    if command == "list":
        list_skills(skills_dir)
    elif command == "validate":
        validate_all_skills(skills_dir)
    elif command == "create":
        if len(sys.argv) < 4:
            print("Usage: create <name> <description>")
            return
        
        skill_name = sys.argv[2]
        description = sys.argv[3]
        
        # Validate name and description
        name_valid, name_msg = validate_skill_name(skill_name)
        if not name_valid:
            print(f"❌ Invalid name: {name_msg}")
            return
        
        desc_valid, desc_msg = validate_description(description)
        if not desc_valid:
            print(f"❌ Invalid description: {desc_msg}")
            return
        
        # Check if skill already exists
        skill_path = skills_dir / skill_name
        if skill_path.exists():
            print(f"❌ Skill '{skill_name}' already exists")
            return
        
        # Ask which template
        print("Select template:")
        templates = get_skill_templates()
        for key, template in templates.items():
            print(f"  {key}. {template['name']}")
        
        template_choice = input("Enter template number (or 'custom'): ")
        
        if template_choice in templates:
            template = templates[template_choice]["content"]
        else:
            # Custom skill
            print("Creating custom skill...")
            template = f"""---
name: {skill_name}
description: {description}
license: Apache-2.0
metadata:
  category: agents
  tags: [ai, agent]
---

# {skill_name}

This skill provides {description}.

## Usage

Use the `/skill` command in OpenCode or Cursor to load this skill.
"""
        template_choice
    elif command == "scan":
        scan_and_update_skills(skills_dir)
    else:
        print(f"❌ Unknown command: {command}")

def validate_all_skills(skills_dir: Path) -> None:
    """Validate all skills in the directory."""
    print("🔍 Validating skills...")
    
    valid_count = 0
    error_count = 0
    
    skill_dirs = [d for d in skills_dir.iterdir() if d.is_dir()]
    
    for skill_dir in skill_dirs:
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue
        
        try:
            with open(skill_file, 'r') as f:
                content = f.read()
                frontmatter = content.split('---')[1] if '---' in content else ''
                data = yaml.safe_load(frontmatter)
                
                # Validate required fields
                if 'name' not in data:
                    print(f"  ❌ {skill_dir.name}: Missing name")
                    error_count += 1
                elif 'description' not in data:
                    print(f"  ❌ {skill_dir.name}: Missing description")
                    error_count += 1
                else:
                    name_valid, name_msg = validate_skill_name(data['name'])
                    if not name_valid:
                        print(f"  ❌ {skill_dir.name}: {name_msg}")
                        error_count += 1
                    else:
                        desc_valid, desc_msg = validate_description(data['description'])
                        if not desc_valid:
                            print(f"  ❌ {skill_dir.name}: {desc_msg}")
                            error_count += 1
                        else:
                            valid_count += 1
        except Exception as e:
            print(f"  ❌ {skill_dir.name}: Error reading - {e}")
            error_count += 1
    
    print(f"\n📊 Summary:")
    print(f"  Valid skills: {valid_count}")
    print(f"  Skills with errors: {error_count}")

def scan_and_update_skills(skills_dir: Path) -> None:
    """Scan skills directory and update tool configuration."""
    print("🔍 Scanning skills directory...")
    
    # Create .opencode/skills if it doesn't exist
    opencode_skills = Path(".opencode/skills")
    opencode_skills.mkdir(parents=True, exist_ok=True)
    
    # Copy skills
    skill_dirs = [d for d in skills_dir.iterdir() if d.is_dir()]
    
    for skill_dir in skill_dirs:
        skill_file = skill_dir / "SKILL.md"
        if skill_file.exists():
            target_path = opencode_skills / skill_dir.name
            target_path.mkdir(parents=True, exist_ok=True)
            
            import shutil
            shutil.copytree(skill_dir, target_path)
            print(f"  📁 Copied {skill_dir.name} to .opencode/skills/")

if __name__ == "__main__":
    main()