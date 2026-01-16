# Cursor Rules Examples

Example cursor rules for previewing and demonstrating how to structure AI coding guidelines.

## What's Included

This directory contains comprehensive examples of cursor rules that demonstrate:

1. **Modular Rules Structure** - Separate files for TypeScript, React, Testing, and Security
2. **YAML Frontmatter** - Metadata for globs, priority, and application settings
3. **Real-world Examples** - Practical coding standards and best practices
4. **Project Overview** - High-level project guidelines
5. **Legacy Format Support** - Single-file `.cursorrules` format

## Quick Start

### Option 1: Use with OpenCode
1. Copy the entire `cursor-rules-examples/` directory to your project root
2. OpenCode will automatically detect and load these rules
3. Rules apply to all AI interactions in your project

### Option 2: Use with Cursor
1. Copy the entire `cursor-rules-examples/` directory to your project root
2. Restart Cursor to reload the rules
3. Rules apply to all AI interactions in your project

## File Structure

```
cursor-rules-examples/
├── .cursorrules/
│   ├── index.mdc              # Project overview (always loaded)
│   ├── typescript.mdc          # TypeScript coding standards
│   ├── react.mdc               # React component guidelines
│   ├── testing.mdc             # Testing best practices
│   └── security.mdc            # Security best practices
├── .cursorrules                  # Legacy single-file format (still works)
└── README.md                   # This file
```

## Examples Overview

### TypeScript Rules (`.cursorrules/typescript.mdc`)
- Naming conventions (PascalCase, camelCase, kebab-case, UPPER_SNAKE_CASE)
- Code organization (one module per file, barrel exports)
- Type safety (strict mode, explicit returns, no `any` types)
- Async/await patterns
- Import organization
- Error handling with custom error classes
- Arrow functions, template literals, const/let

### React Rules (`.cursorrules/react.mdc`)
- Component structure with explicit interfaces
- Functional components with `React.FC`
- Hooks best practices (`useCallback`, `useMemo`)
- State management guidelines
- Styling best practices (CSS modules, no inline styles)
- Performance optimization (lazy loading, code splitting)

### Testing Rules (`.cursorrules/testing.mdc`)
- Test organization (mirror source structure)
- AAA pattern (Arrange, Act, Assert, Annihilate, Repeat)
- Descriptive test naming
- Testing normal, edge cases, and errors
- Mock file structure
- Test commands and running tests

### Security Rules (`.cursorrules/security.mdc`)
- Authentication & authorization (no hardcoded secrets)
- Input validation and sanitization
- Data protection (hashing, encryption, PII handling)
- API security (rate limiting, CORS, CSRF tokens)
- Third-party dependency management (npm audit, security advisories)

### Project Overview (`.cursorrules/index.mdc`)
- Technology stack overview
- Development guidelines (code style, structure, activities, testing)
- Project structure visualization
- Documentation best practices

### Legacy Format (`.cursorrules`)
- Single-file markdown format
- Technology stack description
- Development guidelines for Temporal + OpenAI integration

## Customizing These Examples

To adapt these examples for your own project:

1. **Modify glob patterns**: Change the `globs` in YAML frontmatter to match your file structure
2. **Adjust priorities**: Set `priority: high` for critical rules, `low` for guidelines
3. **Edit content**: Update the rule descriptions to match your project's standards
4. **Add new files**: Create additional `.mdc` files for new domains (e.g., `python.mdc`, `vue.mdc`)
5. **Use conditional application**: Set `alwaysApply: false` to apply rules only when needed (e.g., security checks only on API files)

## Integration with Your Projects

### For the Temporal OpenAI SDK Project
You could add these rules to your project:

```bash
# Copy TypeScript rules to your project
cp -r cursor-rules-examples/.cursorrules/typescript.mdc /path/to/your/project/.cursorrules/

# Copy React rules if you use React
cp -r cursor-rules-examples/.cursorrules/react.mdc /path/to/your/project/.cursorrules/

# Create project-specific overview
cat > /path/to/your/project/.cursorrules/index.mdc << 'EOF'
---
alwaysApply: true
priority: low
description: |
  Your project description here
EOF
```

## Additional Resources

- [Cursor Rules Documentation](https://cursor.sh/docs/rules)
- [OpenCode Rules Documentation](https://opencode.ai/docs/config/)
- [OpenCode Plugin Ecosystem](https://opencode.ai/docs/ecosystem/)

## Contributing

Feel free to modify these examples and share your own cursor rules patterns!
