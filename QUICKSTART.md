# Quick Start Guide

Get started with Temporal and OpenAI Agents SDK in minutes!

### Option 1: Using OpenAI (Standard)

1. Add to `.env` file:
```bash
OPENAI_API_KEY=sk-your-openai-key
```

2. Follow the standard setup instructions

### Option 2: Using OpenRouter - Free Alternative 🆓

OpenRouter provides access to **free AI models** like DeepSeek R1.

**Complete separate implementation** - no conflicts with OpenAI setup!

```bash
# Navigate to OpenRouter folder
cd open-router

# Create .env with your free API key
echo "OPENROUTER_API_KEY=sk-or-v1-your-key" > .env

# Run the example
python example.py
```

See the [open-router/README.md](open-router/README.md) for complete documentation.

## 1. Setup

```bash
# Clone the repository (if you haven't already)
git clone https://github.com/yasinnerten/temporal-openai-agents-sdk.git
cd temporal-openai-agents-sdk

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your OpenAI API key
```

## 2. Start Temporal Server

### Option A: Using Docker (Need to has preconfigured mysql, cassandra or postgres)
```bash
docker run -d -p 7233:7233 -p 8233:8233 -e DB=cassandra temporalio/auto-setup:latest
```

### Option B: Using Temporal CLI (Recommended)
Temporal CLU uses SQLite as the default in-memory database for local development which is lightweight.

```bash
# Install Temporal CLI
brew install temporal  # macOS
# or download from https://docs.temporal.io/cli

# Start development server
temporal server start-dev
```

## 3. Try the Examples

### Example 1: Basic Temporal Workflow

```bash
# Terminal 1: Start the worker
cd examples/temporal
python worker.py

# Terminal 2: Run the workflow
python run_workflow.py
```

Expected output:
```
Workflow result: Hello, Temporal User!
```

### Example 2: OpenAI Basic Agent

```bash
cd examples/openai
python basic_agent.py
```

Expected output:
```
OpenAI Response:
Temporal is a workflow orchestration platform that enables developers to build...
```

### Example 3: Integration (Temporal + OpenAI)

```bash
# Terminal 1: Start the integration worker
cd examples/integration
python worker.py

# Terminal 2: Run the integrated workflow
python run_workflow.py
```

Expected output:
```
Workflow completed!
Generated text: Temporal provides benefits such as...
Character count: 142
Word count: 23
```

## Next Steps

- Read the [full README.md](README.md)
- Check out [Temporal documentation](https://docs.temporal.io/)
- Explore [OpenAI API documentation](https://platform.openai.com/docs/)
- Add your own examples!

## Documentation

- [OpenRouter Integration Guide](docs/open-router-usage.md) - Use free AI models
- [API Documentation](docs/API.md)
- [Examples](examples/)
