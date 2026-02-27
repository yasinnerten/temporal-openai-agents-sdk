#!/usr/bin/env python3
"""Add skills to .opencode configuration automatically."""

import os
import sys
from pathlib import Path
import yaml

def update_agents_md(skills_dir: Path) -> None:
    """Update AGENTS.md with skill information."""
    agents_md = Path("AGENTS.md")
    
    if not agents_md.exists():
        agents_md.write_text("# Skills\n\n")
        agents_md.write_text("This directory contains Agent Skills that work with OpenCode.\n\n")
        agents_md.write_text("## Available Skills\n\n")
    
    # Read skills directory
    skills = []
    skill_dirs = [d for d in skills_dir.iterdir() if d.is_dir()]
    
    for skill_dir in skill_dirs:
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
                print(f"Error reading {skill_file}: {e}")
    
    if skills:
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
        new_content.extend(lines[skills_start:])
        
        # Add skills section
        new_content.append("## Available Skills\n\n")
        
        for skill in sorted(skills, key=lambda x: x['name']):
            new_content.append(f"### {skill['name']}\n")
            new_content.append(f"**Description:** {skill['description']}\n")
            new_content.append(f"**Location:** `{skill['path']}`\n\n")
        
        new_content.extend(["\n## Usage\n\n"])
        new_content.append("To use a skill with OpenCode, use the `/skill` command:\n")
        new_content.append("```bash\n")
        new_content.append("/skill <skill-name>\n")
        new_content.append("```\n\n")
        new_content.extend([
            "## Tool Configuration\n\n",
            "The skills are automatically discovered by OpenCode in the `.opencode/skills/` directory.\n",
            "No additional configuration is required."
        ])
        
        agents_md.write_text("\n".join(new_content))
        print(f"✅ Updated AGENTS.md with {len(skills)} skills")

def main():
    """Main function."""
    skills_dir = Path("skills")
    
    if not skills_dir.exists():
        print("❌ Skills directory not found")
        return
    
    update_agents_md(skills_dir)
    print("✅ Skills directory scanned and AGENTS.md updated")

if __name__ == "__main__":
    main()