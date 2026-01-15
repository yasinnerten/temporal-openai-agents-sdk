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

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yasinnerten/temporal-openai-agents-sdk.git
cd temporal-openai-agents-sdk
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key and Temporal connection details
```

## Running Temporal Server Locally

If you don't have Temporal running, you can start it locally using Docker:

```bash
docker run -d -p 7233:7233 temporalio/auto-setup:latest
```

Or use the Temporal CLI:
```bash
temporal server start-dev
```

## Project Structure

```
temporal-openai-agents-sdk/
├── examples/
│   ├── temporal/           # Basic Temporal workflow examples
│   ├── openai/             # OpenAI SDK examples
│   └── integration/        # Combined Temporal + OpenAI examples
├── requirements.txt        # Project dependencies
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
```

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

Feel free to add your own examples and experiments!

## License

MIT