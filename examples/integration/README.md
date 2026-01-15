# Integration Examples

Examples combining Temporal workflows with OpenAI capabilities.

## Files

- `workflows.py` - Temporal workflow that uses OpenAI within activities
- `worker.py` - Worker that handles AI-powered workflows
- `run_workflow.py` - Executes an AI content generation workflow

## Setup

1. Make sure you have a Temporal server running:
   ```bash
   temporal server start-dev
   ```

2. Set up your `.env` file with both Temporal and OpenAI configuration:
   ```bash
   cp ../../.env.example ../../.env
   ```

3. Add your OpenAI API key to the `.env` file.

## Running the Examples

1. Start the worker:
   ```bash
   python worker.py
   ```

2. In another terminal, run the workflow:
   ```bash
   python run_workflow.py
   ```

## What You'll Learn

- How to integrate OpenAI API calls within Temporal activities
- How to handle external API calls in workflows
- How to build durable AI-powered workflows
- How to implement retry logic for AI operations
- How to process and analyze AI-generated content

## Use Cases

This pattern is useful for:
- Content generation workflows
- AI-powered data processing pipelines
- Automated customer service systems
- Document analysis and summarization
- Multi-step AI reasoning tasks
