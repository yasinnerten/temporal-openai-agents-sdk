# Quick Start Guide

Get started with Temporal and OpenAI Agents SDK in minutes!

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

### Option A: Using Docker (Recommended)
```bash
docker run -d -p 7233:7233 -p 8233:8233 temporalio/auto-setup:latest
```

### Option B: Using Temporal CLI
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

## 4. Explore and Learn

- Check out the code in `examples/` directories
- Read the README.md in each example folder
- Modify the examples to experiment
- Try the Temporal Web UI at http://localhost:8233

## Troubleshooting

### "Connection refused" error
- Make sure Temporal server is running
- Check that port 7233 is not blocked

### "OpenAI API key not found"
- Make sure you've created .env file from .env.example
- Add your OpenAI API key to the .env file

### Import errors
- Make sure you're in the virtual environment
- Run `pip install -r requirements.txt`

## Next Steps

- Read the [full README.md](README.md)
- Check out [Temporal documentation](https://docs.temporal.io/)
- Explore [OpenAI API documentation](https://platform.openai.com/docs/)
- Add your own examples!
