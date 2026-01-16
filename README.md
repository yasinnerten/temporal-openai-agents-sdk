# Temporal & OpenAI Agents SDK Testing Repository

A repository for testing and learning [Temporal](https://temporal.io/) workflow orchestration and [OpenAI Agents SDK](https://github.com/openai/openai-python).

## Overview

This repository contains examples and experiments combining:
- **Temporal**: A durable workflow orchestration platform for building reliable applications
- **OpenAI Agents SDK**: OpenAI's Python SDK for building AI agents and integrations

## Prerequisites

- Python 3.8 or higher
- A running Temporal server (local or cloud)
- OpenAI API key

## Quick Start


# 1. Clone and setup
git clone https://github.com/yasinnerten/temporal-openai-agents-sdk.git
cd temporal-openai-agents-sdk
python -m venv venv && source venv/bin/activate

# 2. Install and configure
pip install -r requirements.txt
```
cp .env.example .env && vim .env
# Edit .env and add your OpenAI API key and Temporal connection details
# Or using make
make install
```
# 3. Start Temporal server
temporal server start-dev

# 4. Run an example (in new terminal)
python examples/integration/run_workflow.py
```

## Running Temporal Server Locally

If you don't have Temporal running, you can start it locally using Docker:
But then you need to set a database, since container doesn't have option for sql-lite

```bash
# docker run -d -p 7233:7233 DB=cassandra temporalio/auto-setup:latest
```
or 
```bash
# docker compose up -d
```

# 5. Cleanup and environment check
make check             # Verify environment setup
make test              # Run test suite
make clean             # Remove cache and build files

## Project Structure

```
temporal-openai-agents-sdk/
├── examples/
│   ├── temporal/           # Basic Temporal workflow examples
│   ├── openai/             # OpenAI SDK examples
│   └── integration/        # Combined Temporal + OpenAI examples
├── open-router/            # OpenRouter integration (free models)
├── tests/                  # Test suite
├── Makefile               # Build automation
├── requirements.txt        # Project dependencies
├── check_setup.py         # Verify environment setup
├── pyproject.toml         # Project configuration
└── README.md              # This file
```

## Examples

### Running Temporal Examples

```bash
# Start a worker
python examples/temporal/worker.py

# In another terminal, run a workflow
python examples/temporal/run_workflow.py
```

### Running OpenAI Examples

```bash
python examples/openai/basic_agent.py
```

### Running Integration Examples

```bash
# Start the Temporal worker with OpenAI integration
python examples/integration/worker.py

# Run the integrated workflow
python examples/integration/run_workflow.py

# Start the worker for multi-step AI chain
python examples/integration/multi_step_chain_worker.py

# Run the multi-step AI chain workflow (generation → analysis → summary → extraction)
python examples/integration/run_multi_step_chain.py
```

## Extending the SDK

### Creating Custom Workflows

1. **Define workflow logic** in `examples/integration/`:
   - Inherit from Temporal's `WorkflowBase`
   - Use `@workflow.run` decorator for workflow methods
   - Define activities for long-running tasks

2. **Integrate OpenAI Agents**:
   - Create activity methods that call OpenAI Agents SDK
   - Handle tool calls and agent responses asynchronously
   - Chain multiple agent calls within workflow logic

3. **Add custom activities**:
   ```python
   @activity.defn
   async def my_custom_activity(input_data: str) -> str:
       # Your implementation here
       return result
   ```

### Building Your Own Agents

- Extend the examples in `examples/openai/` with custom tools
- Use Temporal workflows to orchestrate multi-step agent tasks
- Combine with other APIs and data sources

### Testing Locally

- Use Temporal's local development server
- Mock OpenAI responses for unit tests
- Test workflow logic with different scenarios

## Learning Resources

### Temporal
- [Temporal Documentation](https://docs.temporal.io/)
- [Temporal Python SDK](https://github.com/temporalio/sdk-python)
- [Temporal Samples](https://github.com/temporalio/samples-python)

### OpenAI
- [OpenAI API Documentation](https://platform.openai.com/docs/api-reference)
- [OpenAI Python SDK](https://github.com/openai/openai-python)
- [OpenAI Cookbook](https://cookbook.openai.com/)

## Contributing

Feel free to add your own examples and experiments! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

This repo created with help from copilot-swe-agent and Claude Haiku 3.5.

## License

MIT