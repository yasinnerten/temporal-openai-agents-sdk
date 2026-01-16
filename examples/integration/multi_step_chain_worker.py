"""
Worker for the multi-step AI chain workflow.

This worker handles the MultiStepAIChainWorkflow and its associated activities.
"""

import asyncio
import os
from dotenv import load_dotenv
from temporalio.client import Client
from temporalio.worker import Worker

from multi_step_chain import (
    MultiStepAIChainWorkflow,
    generate_content,
    analyze_content,
    summarize_analysis,
    extract_key_points,
)

# Load environment variables
load_dotenv()


async def main():
    """Start the Temporal worker for multi-step AI chain."""
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
        task_queue="multi-step-ai-chain-queue",
        workflows=[MultiStepAIChainWorkflow],
        activities=[
            generate_content,
            analyze_content,
            summarize_analysis,
            extract_key_points,
        ],
    )

    print(f"Worker started on task queue: multi-step-ai-chain-queue")
    print(f"Temporal host: {temporal_host}")
    print("Waiting for workflows...")

    # Run the worker
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
