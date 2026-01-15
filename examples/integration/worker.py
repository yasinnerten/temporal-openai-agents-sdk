"""
Temporal worker with OpenAI integration.

This worker handles workflows that use OpenAI.
"""

import asyncio
import os
from dotenv import load_dotenv
from temporalio.client import Client
from temporalio.worker import Worker

from workflows import AIContentWorkflow, generate_text_with_openai, process_response

# Load environment variables
load_dotenv()


async def main():
    """Start the Temporal worker with OpenAI integration."""
    # Get Temporal configuration from environment
    temporal_host = os.getenv("TEMPORAL_HOST", "localhost:7233")
    temporal_namespace = os.getenv("TEMPORAL_NAMESPACE", "default")

    # Verify OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("Warning: OPENAI_API_KEY not found in environment variables")
        print("Please copy .env.example to .env and add your API key")
        return

    # Connect to Temporal
    client = await Client.connect(
        temporal_host,
        namespace=temporal_namespace,
    )

    # Create worker
    worker = Worker(
        client,
        task_queue="ai-content-task-queue",
        workflows=[AIContentWorkflow],
        activities=[generate_text_with_openai, process_response],
    )

    print(f"Worker started on task queue: ai-content-task-queue")
    print(f"Temporal host: {temporal_host}")
    print("Waiting for workflows...")

    # Run the worker
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
