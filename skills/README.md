# Agent Skills

This directory contains Agent Skills that work with OpenCode, Cursor, Claude Code, and other Agent Skills-compatible platforms.

## What Are Agent Skills?

Agent Skills are folders of instructions, scripts, and resources that AI coding agents can discover and use on-demand. Think of them as "onboarding documents" for AI assistants.

**Key Benefits:**
- **Reusable**: Create once, use across multiple conversations and projects
- **Cross-platform**: Same skills work across OpenCode, Cursor, Claude Code, VS Code, and more
- **Progressive disclosure**: Agents load only relevant skills when needed, preventing context window overload
- **Shareable**: Skills can be shared with teams and version-controlled

## Directory Structure

```
skills/
├── temporal-workflows/
│   ├── SKILL.md
│   ├── scripts/
│   │   ├── setup.sh
│   │   └── test.sh
│   └── references/
│       └── temporal-patterns.md
├── openai-agents/
│   ├── SKILL.md
│   ├── scripts/
│   │   ├── setup.sh
│   │   └── test.sh
│   └── references/
│       └── openai-patterns.md
├── python-best-practices/
│   ├── SKILL.md
│   ├── scripts/
│   │   ├── setup.sh
│   │   └── lint.sh
│   └── references/
│       └── python-standards.md
├── go-backend-tool/
│   ├── SKILL.md
│   ├── scripts/
│   │   ├── setup.sh
│   │   └── build.sh
│   └── references/
│       └── go-patterns.md
├── docker-containerization/
│   ├── SKILL.md
│   ├── scripts/
│   │   ├── build.sh
│   │   └── deploy.sh
│   └── references/
│       └── docker-standards.md
├── frontend-implementation/
│   ├── SKILL.md
│   ├── scripts/
│   │   ├── setup.sh
│   │   └── build.sh
│   └── references/
│       └── react-vue-patterns.md
└── agent-implementation/
    ├── SKILL.md
    └── references/
        ├── agent-patterns.md
        └── memory-systems.md
└── README.md
```

## Available Skills

### 1. [Temporal Workflows](./temporal-workflows/SKILL.md)
Comprehensive guide for Temporal workflow orchestration including:
- Activity design principles (idempotency, deterministic)
- Error handling and retry policies
- Signal handling and cancellation
- Testing strategies
- Performance optimization
- Heartbeat activities and caching
- Context management

**Topics Covered:**
- Workflow design patterns
- Activity best practices
- Retry policies (transient vs non-retryable errors)
- Testing (unit, workflow, integration)
- Performance optimization
- Debugging and monitoring

**Use When:**
- Building Temporal workflows for AI agent orchestration
- Implementing multi-step processes with OpenAI agents
- Working with activities and task queues
- Testing durable workflow execution

### 2. [OpenAI Agents](./openai-agents/SKILL.md)
Complete guide for integrating OpenAI Agents SDK with Temporal workflows:

**Setup and Configuration:**
- Installation and environment setup
- API key management
- Client initialization patterns
- Configuration management with Viper

**Basic Usage:**
- Chat completions
- Streaming responses
- Function calling
- Autonomous agent workflows
- Multi-step reasoning

**Error Handling:**
- Rate limiting with exponential backoff
- Token management and cost optimization
- Input sanitization
- Secrets management

**Integration with Temporal:**
- Activity definitions
- Workflow integration
- Worker configuration
- Query methods

**Testing:**
- Mocking OpenAI responses
- Integration testing
- Usage tracking and metrics

**Use When:**
- Building AI agents with OpenAI SDK
- Integrating OpenAI with Temporal for durable execution
- Managing API costs and rate limits
- Testing AI agent workflows

### 3. [Python Best Practices](./python-best-practices/SKILL.md)
Comprehensive Python coding standards and best practices:

**Code Style:**
- PEP 8 compliance (indentation, line length, import order)
- Type hints and docstrings
- Dataclasses and data structures
- List comprehensions and generators

**Error Handling:**
- Specific exceptions and validation
- Context managers and resource cleanup
- Logging and structured logging

**Data Structures:**
- Efficient data processing
- Lazy loading patterns
- Caching strategies

**Concurrency:**
- Async/await patterns
- Threading and ThreadPoolExecutor
- WaitGroup for coordination

**Testing:**
- Unit tests with pytest
- Fixtures and parametrized tests
- Integration testing
- Performance optimization

**Security:**
- Input validation and sanitization
- Secrets management with keyring
- File permissions

**Use When:**
- Writing clean, maintainable Python code
- Working with AI-assisted development
- Implementing testing and CI/CD

### 4. [Go Backend Tool](./go-backend-tool/SKILL.md)
Complete Go backend development patterns:

**Standard Layouts:**
- HTTP handlers and routing
- Database layer with PostgreSQL
- Middleware (logging, auth, CORS)
- Configuration management

**Error Handling:**
- Custom errors with HTTP codes
- Graceful shutdown patterns
- Panic recovery

**Database Patterns:**
- Transaction management
- Connection pooling
- Query optimization

**Testing:**
- Table-driven tests
- Mocks with interfaces
- Parametrized tests

**API Design:**
- RESTful endpoints
- Pagination strategies
- Health checks

**Deployment:**
- Dockerfile patterns (multi-stage, optimization)
- Docker Compose configurations
- Kubernetes deployment
- Docker registry and security scanning

**Use When:**
- Building Go backends and APIs
- Implementing database integrations
- Setting up containerization
- Writing Go tests and deployment

### 5. [Docker Containerization](./docker-containerization/SKILL.md)
Docker and container orchestration patterns:

**Multi-Stage Builds:**
- Python, Go, and Node.js patterns
- Alpine Linux base images
- Layer caching and optimization

**Docker Compose:**
- Basic and multi-service setups
- Development environment configuration
- Health check patterns

**Best Practices:**
- Minimal base images
- Non-root user
- Health checks and signal handling
- Resource limits and security

**Kubernetes:**
- Deployment and Service YAMLs
- ConfigMaps and Secrets
- Liveness and readiness probes

**Docker Registry:**
- Docker Hub and private registry pushes
- Orchestration (Docker Swarm, Nomad)

**Optimization:**
- BuildKit caching
- Parallel builds
- Image size reduction

**Use When:**
- Containerizing applications
- Setting up Docker Compose development environments
- Deploying to Kubernetes
- Building optimized Docker images

### 6. [Frontend Implementation](./frontend-implementation/SKILL.md)
Modern frontend development patterns:

**React Development:**
- Component architecture and props
- Custom hooks (useLocalStorage, useMemo)
- Performance optimization (memoization, code splitting)
- State management with Context API
- Routing with React Router
- Forms and validation
- API integration
- TypeScript integration

**Vue Development:**
- Composition API
- Reactive state with Pinia
- Router integration
- Components and templates

**Modern JavaScript:**
- ES modules and async/await
- Error handling patterns
- Virtual scrolling and code splitting

**TypeScript:**
- Type definitions and generics
- Generic utilities

**CSS/Styling:**
- CSS-in-JS patterns
- CSS modules
- Accessibility (ARIA labels, keyboard navigation)

**Testing:**
- React Testing Library
- Component testing
- E2E testing with Cypress

**Deployment:**
- Vite and Next.js builds
- Static site generation

**Use When:**
- Building React, Vue, or vanilla JavaScript applications
- Implementing modern frontend patterns
- Setting up development and build workflows
- Testing frontend applications

### 7. [Agent Implementation](./agent-implementation/SKILL.md)
Complete guide for implementing AI agents:

**Core Concepts:**
- Agent architecture (reasoning engine, memory, tool registry)
- Agent types (reactive, proactive, multi-agent)
- Stateful vs stateless agents

**Basic Patterns:**
- Simple tool-using agents
- Stateful agents with persistence
- Specialized agents (code, research)

**Multi-Agent Systems:**
- Agent orchestration
- Specialized agents collaboration
- Task classification and routing

**Tool Calling:**
- Function definitions and execution
- Tool selection and parameter extraction

**Memory Systems:**
- Short-term memory (limited context window)
- Long-term memory (vector stores)
- Hybrid memory systems

**Error Handling:**
- Retry with exponential backoff
- Fallback mechanisms
- Graceful degradation

**Monitoring and Observability:**
- Structured logging
- Metrics collection
- Distributed tracing

**Temporal Integration:**
- Workflow activities
- Durable execution
- Worker configuration

**Testing:**
- Unit tests
- Integration tests

**Best Practices:**
- Design patterns
- Error handling
- Performance optimization
- Security
- Testability

**Use When:**
- Building AI agents with memory and tool capabilities
- Implementing multi-agent systems
- Monitoring agent behavior
- Testing agent workflows

## How to Use These Skills

### With OpenCode
1. Copy this directory to your project root
2. OpenCode automatically discovers skills in `.opencode/skill/<name>/SKILL.md`
3. Use `/skill` command to list and load skills
4. Skills are loaded on-demand when relevant

### With Cursor
1. Copy this directory to your project root
2. Cursor discovers skills in `.claude/skills/<name>/SKILL.md`
3. Skills are available in Composer (agent mode)

### With Claude Code
1. Copy this directory to your project root
2. Claude Code automatically discovers skills in `.claude/skills/<name>/SKILL.md`
3. Use the skill discovery command to load relevant skills

### Creating Your Own Skills

Follow the [Agent Skills Specification](https://agentskills.io/specification):

1. Create a folder for your skill
2. Add a `SKILL.md` file with YAML frontmatter
3. Optional: Add `scripts/`, `references/`, `assets/` directories

**SKILL.md Format:**
```yaml
---
name: skill-name
description: A description of what this skill does and when to use it.
license: Apache-2.0
metadata:
  category: development
  tags: [python, testing]
---
# Your skill content here
```

**Required Fields:**
- `name`: 1-64 characters, lowercase alphanumeric with hyphens
- `description`: 1-1024 characters

**Optional Fields:**
- `license`: License name
- `compatibility`: Environment requirements
- `metadata`: String-to-string map for custom metadata

## Best Practices

### Skill Design
- **Keep it focused**: Each skill should solve a specific problem well
- **Make it modular**: Break complex skills into smaller, composable pieces
- **Provide examples**: Show how to use the skill
- **Version your skills**: Use semantic versioning when skills evolve

### Writing Documentation
- **Start with a clear description**: What does this skill do?
- **Provide code examples**: Show the skill in action
- **Include troubleshooting**: Common issues and solutions
- **Document dependencies**: What libraries and tools are required?

### Testing Skills
- **Write unit tests**: Test your skill's components independently
- **Test with OpenCode**: Verify skills work as expected
- **Test with Cursor**: Ensure compatibility with other tools

## Additional Resources

- [Agent Skills Specification](https://agentskills.io/specification)
- [OpenCode Skills Documentation](https://opencode.ai/docs/skills/)
- [Claude Skills Documentation](https://support.claude.com/en/articles/12512176-what-are-skills)
- [OpenAI Agents Documentation](https://platform.openai.com/docs/guides/agents)
- [Anthropic Agent Skills](https://anthropics.com/agentskills)

## Contributing

Have a skill you'd like to share? Submit a pull request or open an issue on the [Agent Skills repository](https://github.com/agentskills/agentskills).

## License

All skills in this directory are licensed under the Apache 2.0 License unless otherwise specified in the SKILL.md file.
