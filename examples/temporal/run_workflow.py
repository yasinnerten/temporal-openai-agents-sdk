"""
Run a Temporal workflow example.

This script starts a workflow and waits for the result.
"""

import asyncio
import os
from temporalio.client import Client

from workflows import GreetingWorkflow


async def main():
    """Run the workflow."""
    # Get Temporal configuration from environment
    temporal_host = os.getenv("TEMPORAL_HOST", "localhost:7233")
    temporal_namespace = os.getenv("TEMPORAL_NAMESPACE", "default")

    # Connect to Temporal
    client = await Client.connect(
        temporal_host,
        namespace=temporal_namespace,
    )

    # Start the workflow
    print("Starting GreetingWorkflow...")
    result = await client.execute_workflow(
        GreetingWorkflow.run,
        "Temporal User",
        id="greeting-workflow-1",
        task_queue="greeting-task-queue",
    )

    print(f"Workflow result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
