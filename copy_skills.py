#!/usr/bin/env python3
"""Tool to update .opencode/skills and .claude/skills with discovered skills."""

import os
import sys
import yaml
from pathlib import Path

def copy_skills_to_opencode():
    """Copy skills to .opencode/skills directory."""
    skills_dir = Path("skills")
    if not skills_dir.exists():
        print("❌ Skills directory not found")
        return
    
    opencode_skills_dir = Path(".opencode/skills")
    opencode_skills_dir.mkdir(parents=True, exist_ok=True)
    
    claude_skills_dir = Path(".claude/skills")
    claude_skills_dir.mkdir(parents=True, exist_ok=True)
    
    skills_copied = 0
    
    for skill_dir in skills_dir.iterdir():
        if skill_dir.is_dir():
            skill_file = skill_dir / "SKILL.md"
            if skill_file.exists():
                try:
                    with open(skill_file, 'r') as f:
                        content = f.read()
                        frontmatter = content.split('---')[1] if '---' in content else ''
                        data = yaml.safe_load(frontmatter)
                    
                    # Copy to .opencode/skills
                    target_path = opencode_skills_dir / skill_dir.name
                    target_path.mkdir(parents=True, exist_ok=True)
                    
                    for item in skill_dir.iterdir():
                        src = skill_dir / item
                        dst = target_path / item
                        if src.is_file():
                            import shutil
                            shutil.copy2(src, dst)
                    
                    skills_copied += 1
                    print(f"  ✅ {skill_dir.name} -> .opencode/skills")
                    
                except Exception as e:
                    print(f"  ❌ Error copying {skill_dir.name}: {e}")
    
    print(f"\n📊 Copied {skills_copied} skills to .opencode/skills")

def copy_skills_to_claude():
    """Copy skills to .claude/skills directory."""
    skills_dir = Path("skills")
    if not skills_dir.exists():
        print("❌ Skills directory not found")
        return
    
    claude_skills_dir = Path(".claude/skills")
    claude_skills_dir.mkdir(parents=True, exist_ok=True)
    
    skills_copied = 0
    
    for skill_dir in skills_dir.iterdir():
        if skill_dir.is_dir():
            skill_file = skill_dir / "SKILL.md"
            if skill_file.exists():
                try:
                    with open(skill_file, 'r') as f:
                        content = f.read()
                        frontmatter = content.split('---')[1] if '---' in content else ''
                        data = yaml.safe_load(frontmatter)
                    
                    # Copy to .claude/skills
                    target_path = claude_skills_dir / skill_dir.name
                    target_path.mkdir(parents=True, exist_ok=True)
                    
                    for item in skill_dir.iterdir():
                        src = skill_dir / item
                        dst = target_path / item
                        if src.is_file():
                            import shutil
                            shutil.copy2(src, dst)
                    
                    skills_copied += 1
                    print(f"  ✅ {skill_dir.name} -> .claude/skills")
                    
                except Exception as e:
                    print(f"  ❌ Error copying {skill_dir.name}: {e}")
    
    print(f"\n📊 Copied {skills_copied} skills to .claude/skills")

def update_agents_md():
    """Update AGENTS.md with skill information."""
    skills_dir = Path("skills")
    agents_md = Path("AGENTS.md")
    
    if not skills_dir.exists():
        print("❌ Skills directory not found")
        return
    
    skills = []
    
    for skill_dir in skills_dir.iterdir():
        if skill_dir.is_dir():
            skill_file = skill_dir / "SKILL.md"
            if skill_file.exists():
                try:
                    with open(skill_file, 'r') as f:
                        content = f.read()
                        frontmatter = content.split('---')[1] if '---' in content else ''
                        data = yaml.safe_load(frontmatter)
                    
                    skills.append({
                        'name': data.get('name', skill_dir.name),
                        'description': data.get('description', 'No description'),
                        'path': skill_dir.relative_to(Path.cwd())
                    })
                except Exception as e:
                    print(f"  ❌ Error reading {skill_dir.name}: {e}")
    
    if not skills:
        print("❌ No skills found")
        return
    
    # Update AGENTS.md
    content = agents_md.read_text()
    lines = content.split('\n')
    
    # Find the line with skills
    skills_start = -1
    for i, line in enumerate(lines):
        if line.startswith("## Available Skills"):
            skills_start = i + 1
            break
    
    if skills_start == -1:
        skills_start = len(lines)
    
    # Replace content after "Available Skills"
    new_content = lines[:skills_start]
    new_content.extend(["\n"])
    new_content.append("## Available Skills\n\n")
    
    for skill in sorted(skills, key=lambda x: x['name']):
        new_content.append(f"### {skill['name']}\n")
        new_content.append(f"**Description:** {skill['description']}\n")
        new_content.append(f"**Location:** `{skill['path']}`\n\n")
    
    new_content.extend(["\n## Usage\n\n"])
    new_content.append("To use a skill with OpenCode, use the `/skill` command:\n")
    new_content.append("```bash\n")
    new_content.append("/skill <skill-name>\n")
    new_content.append("```\n")
    
    new_content.extend(["\n## Tool Configuration\n\n"])
    new_content.append("The skills are automatically discovered by OpenCode in the `.opencode/skills/` directory.\n")
    new_content.append("No additional configuration is required.\n")
    
    agents_md.write_text("\n".join(new_content))
    print("✅ AGENTS.md updated")

def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: python copy_skills.py [opencode|claude|both]")
        return
    
    command = sys.argv[1]
    
    if command in ["opencode", "both"]:
        copy_skills_to_opencode()
    
    if command in ["claude", "both"]:
        copy_skills_to_claude()
    
    if command == "both":
        copy_skills_to_opencode()
        copy_skills_to_claude()
    
    # Always update AGENTS.md after copying
    update_agents_md()

if __name__ == "__main__":
    main()