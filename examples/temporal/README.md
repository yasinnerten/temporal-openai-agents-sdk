# Temporal Examples

Basic examples of using Temporal for workflow orchestration.

## Files

- `workflows.py` - Defines a simple greeting workflow and activity
- `worker.py` - Starts a Temporal worker that executes workflows
- `run_workflow.py` - Triggers a workflow execution

## Running the Examples

1. Make sure you have a Temporal server running:
   ```bash
   temporal server start-dev
   ```

2. Start the worker:
   ```bash
   python worker.py
   ```

3. In another terminal, run the workflow:
   ```bash
   python run_workflow.py
   ```

## What You'll Learn

- How to define Temporal workflows and activities
- How to configure retry policies
- How to start a Temporal worker
- How to execute workflows programmatically
