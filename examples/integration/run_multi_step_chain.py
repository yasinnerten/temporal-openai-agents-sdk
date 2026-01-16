"""
Run the multi-step AI chain workflow.

This script demonstrates running a complex workflow that chains multiple AI operations:
1. Content generation
2. Content analysis
3. Summary creation
4. Key point extraction
"""

import asyncio
import os
from dotenv import load_dotenv
from temporalio.client import Client

from multi_step_chain import MultiStepAIChainWorkflow

# Load environment variables
load_dotenv()


async def main():
    """Run the multi-step AI chain workflow."""
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

    print("=" * 70)
    print("Multi-Step AI Chain Workflow Example")
    print("=" * 70)
    print("\nThis workflow demonstrates chaining multiple AI operations:")
    print("1. Generate content about a topic")
    print("2. Analyze the content")
    print("3. Create a summary")
    print("4. Extract key points")
    print()

    # Example 1: Short content about Temporal
    print("Example 1: Short content about Temporal")
    print("-" * 70)

    result = await client.execute_workflow(
        MultiStepAIChainWorkflow.run,
        "Temporal workflow orchestration",
        "short",
        id="multi-step-chain-1",
        task_queue="multi-step-ai-chain-queue",
    )

    print(f"\nTopic: {result['topic']}")
    print(f"Word Count: {result['content_word_count']}")
    print(f"\nGenerated Content:")
    print(result["generated_content"])
    print(f"\nAnalysis:")
    print(result["analysis"])
    print(f"\nFinal Summary:")
    print(result["final_summary"])
    print(f"\nKey Points:")
    for point in result["key_points"].split(";"):
        print(f"  • {point.strip()}")

    print("\n" + "=" * 70)

    # Example 2: Medium content about Machine Learning
    print("Example 2: Medium content about Machine Learning")
    print("-" * 70)

    result = await client.execute_workflow(
        MultiStepAIChainWorkflow.run,
        "Machine Learning in production systems",
        "medium",
        id="multi-step-chain-2",
        task_queue="multi-step-ai-chain-queue",
    )

    print(f"\nTopic: {result['topic']}")
    print(f"Word Count: {result['content_word_count']}")
    print(f"\nGenerated Content:")
    print(result["generated_content"])
    print(f"\nAnalysis:")
    print(result["analysis"])
    print(f"\nFinal Summary:")
    print(result["final_summary"])
    print(f"\nKey Points:")
    for point in result["key_points"].split(";"):
        print(f"  • {point.strip()}")

    print("\n" + "=" * 70)
    print("Multi-step AI chain workflow completed successfully!")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
