#!/usr/bin/env python3
"""Update tools summary with skill creation functionality."""

import os
import sys
from pathlib import Path

def create_opencode_skills():
    """Create .opencode/skills directory and skills."""
    opencode_dir = Path(".opencode")
    opencode_dir.mkdir(exist_ok=True)
    
    skills_dir = Path("skills")
    opencode_skills_dir = opencode_dir / "skills"
    
    # Copy existing skills
    if skills_dir.exists():
        for skill_dir in skills_dir.iterdir():
            if skill_dir.is_dir():
                skill_path = opencode_skills_dir / skill_dir.name
                opencode_skills_dir.mkdir(parents=True, exist_ok=True)
                
                # Copy entire directory
                for item in skill_dir.iterdir():
                    src = skill_dir / item
                    dst = skill_path / item
                    if src.is_file():
                        import shutil
                        shutil.copy2(src, dst)
                    elif src.is_dir():
                        import shutil
                        shutil.copytree(src, dst)
    
    print("✅ Skills copied to .opencode/skills/")

def main():
    """Main function with all operations."""
    if len(sys.argv) < 2:
        print("Usage: python tools.py [command]")
        print("Commands:")
        print("  create-opencode - Create .opencode/skills directory and copy skills")
        print("  copy-skills - Copy skills to .opencode/skills")
        print("  update-agents - Update AGENTS.md with skill information")
        print("  create-skill - Create a new skill (see create_simple_skill.py)")
        print("  validate - Validate all skills (see validate_skills.py)")
        return
    
    command = sys.argv[1]
    
    if command == "create-opencode":
        create_opencode_skills()
    elif command == "copy-skills":
        create_opencode_skills()
    elif command == "update-agents":
        # Import update_agents module
        from copy_skills import update_agents_md
        update_agents_md()
    elif command == "create-skill":
        # Import create_simple_skill module
        from create_simple_skill import main
        main(sys.argv[2:])
    elif command == "validate":
        # Import validate_skills module
        from validate_skills import validate_all_skills
        validate_all_skills()
    else:
        print(f"❌ Unknown command: {command}")

if __name__ == "__main__":
    main()