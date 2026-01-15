"""
Run the integrated Temporal + OpenAI workflow.

This script starts a workflow that uses OpenAI within Temporal.
"""

import asyncio
import os
from dotenv import load_dotenv
from temporalio.client import Client

from workflows import AIContentWorkflow

# Load environment variables
load_dotenv()


async def main():
    """Run the AI content workflow."""
    # Get Temporal configuration from environment
    temporal_host = os.getenv("TEMPORAL_HOST", "localhost:7233")
    temporal_namespace = os.getenv("TEMPORAL_NAMESPACE", "default")

    # Verify OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not found in environment variables")
        print("Please copy .env.example to .env and add your API key")
        return

    # Connect to Temporal
    client = await Client.connect(
        temporal_host,
        namespace=temporal_namespace,
    )

    # Start the workflow
    print("Starting AIContentWorkflow...")
    print("Prompt: 'Explain the benefits of using Temporal for workflow orchestration'")

    result = await client.execute_workflow(
        AIContentWorkflow.run,
        "Explain the benefits of using Temporal for workflow orchestration in 2-3 sentences.",
        id="ai-content-workflow-1",
        task_queue="ai-content-task-queue",
    )

    print("\nWorkflow completed!")
    print(f"Generated text: {result['original_response']}")
    print(f"Character count: {result['length']}")
    print(f"Word count: {result['word_count']}")


if __name__ == "__main__":
    asyncio.run(main())
