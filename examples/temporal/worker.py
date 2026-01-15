"""
Temporal worker example.

This worker registers and runs workflows and activities.
"""

import asyncio
import os
from temporalio.client import Client
from temporalio.worker import Worker

from workflows import GreetingWorkflow, create_greeting


async def main():
    """Start the Temporal worker."""
    # Get Temporal configuration from environment
    temporal_host = os.getenv("TEMPORAL_HOST", "localhost:7233")
    temporal_namespace = os.getenv("TEMPORAL_NAMESPACE", "default")

    # Connect to Temporal
    client = await Client.connect(
        temporal_host,
        namespace=temporal_namespace,
    )

    # Create worker
    worker = Worker(
        client,
        task_queue="greeting-task-queue",
        workflows=[GreetingWorkflow],
        activities=[create_greeting],
    )

    print(f"Worker started on task queue: greeting-task-queue")
    print(f"Temporal host: {temporal_host}")
    print("Waiting for workflows...")

    # Run the worker
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
