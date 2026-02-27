# 🔧 Skills Development Tools

This directory contains tools for creating, managing, and validating Agent Skills.

## Tools Available

### 1. Skill Creation
- `create_simple_skill.py` - Create new Agent Skills with templates
- `validate_skills.py` - Validate existing skills for syntax and compliance

### 2. Skill Management
- `copy_skills.py` - Copy skills to `.opencode/skills` and `.claude/skills` directories
- `tools.py` - Unified tool for all skill operations

### 3. Validation
- Uses `pyyaml` for parsing YAML frontmatter
- Validates skill names, descriptions, and field constraints
- Follows Agent Skills specification requirements

### 4. Environment Setup
The tools use Python 3 with virtual environment management.

## Quick Start

### Create Your First Skill
```bash
# Create a new skill with template
python tools.py create-skill my-skill "My custom agent for X task"

# Create a web scraping skill
python tools.py create-skill web-scraper "Web scraper for HTML parsing"

# Validate all skills
python tools.py validate
```

### Manage Skills
```bash
# Copy all skills to OpenCode format
python tools.py copy-skills

# Update AGENTS.md with discovered skills
python tools.py update-agents
```

## Development Workflow

1. **Create Skill**: Use `create_simple_skill.py` to create new skills with templates
2. **Test**: Use `validate_skills.py` to ensure compliance
3. **Copy**: Use `copy_skills.py` to copy to OpenCode/Claude directories
4. **Deploy**: Copy the `skills/` directory to your project

## Skill Template Structure

Each skill follows this structure:
```
skill-name/
├── SKILL.md           # Required: Main skill definition
├── scripts/           # Optional: Shell scripts, utilities
└── references/         # Optional: Documentation, templates
```

## Best Practices

1. **Naming**: Use lowercase alphanumeric with hyphens
2. **Description**: Clear, concise (1-1024 characters)
3. **Templates**: Start with provided templates, then customize
4. **Validation**: Always validate before committing

## Installation

```bash
# Clone the skills repository
git clone https://github.com/your-org/your-skills.git

# Navigate to skills directory
cd your-skills

# Create your skill
python create_simple_skill.py my-new-skill "Description of my skill"
```

## Compatibility

Skills created with these tools are compatible with:
- **OpenCode**: Auto-discovery in `.opencode/skill/`
- **Cursor**: Auto-discovery in `.claude/skills/`
- **Claude Code**: Auto-discovery in `.claude/skills/`
- **VS Code**: Manual copy to `.vscode/skills/`

## Contributions

Contributions welcome! Please ensure:
1. Skills follow Agent Skills specification
2. Include comprehensive documentation
3. Add tests for complex skills
4. Validate with provided tools

## License

All tools and skills in this repository are licensed under Apache-2.0.