
"""
Complete example demonstrating OpenRouter integration.
This script shows how to use free DeepSeek R1 model with Temporal.

Usage:
    1. Create .env file with OPENROUTER_API_KEY
    2. Start Temporal: temporal server start-dev
    3. Run: python example.py
"""
import asyncio
from client import get_openrouter_client
from workflows import (
    SimpleAgentWorkflow,
    CodeAssistantWorkflow,
    DataAnalysisWorkflow,
)


async def run_simple_example():
    """Run a basic question-answer example."""
    print("\n" + "="*60)
    print("Example 1: Simple Question")
    print("="*60)
    
    client = await get_openrouter_client()
    
    handle = await client.start_workflow(
        SimpleAgentWorkflow.run,
        "What is Temporal and why is it useful?",
        id="simple-example",
        task_queue="openrouter-queue",
    )
    
    print("⏳ Waiting for response...")
    result = await handle.result()
    
    print("\n🤖 Response:")
    print(result)


async def run_code_assistant_example():
    """Run a coding question example."""
    print("\n" + "="*60)
    print("Example 2: Code Assistant")
    print("="*60)
    
    client = await get_openrouter_client()
    
    handle = await client.start_workflow(
        CodeAssistantWorkflow.run,
        "How do I create an async function in Python that retries on failure?",
        id="code-assistant-example",
        task_queue="openrouter-queue",
    )
    
    print("⏳ Waiting for response...")
    result = await handle.result()
    
    print("\n🤖 Response:")
    print(result)


async def run_data_analysis_example():
    """Run a data analysis example."""
    print("\n" + "="*60)
    print("Example 3: Data Analysis")
    print("="*60)
    
    client = await get_openrouter_client()
    
    handle = await client.start_workflow(
        DataAnalysisWorkflow.run,
        "Analyze the trend: Sales increased 20% in Q1, dropped 5% in Q2, and increased 35% in Q3.",
        id="data-analysis-example",
        task_queue="openrouter-queue",
    )
    
    print("⏳ Waiting for response...")
    result = await handle.result()
    
    print("\n🤖 Response:")
    print(result)


async def main():
    """Run all examples."""
    print("🌐 OpenRouter + Temporal Integration Examples")
    print("Using free DeepSeek R1 model")
    
    try:
        print("\n🔌 Connecting to Temporal with OpenRouter...")
        
        # Run examples
        await run_simple_example()
        await run_code_assistant_example()
        await run_data_analysis_example()
        
        print("\n" + "="*60)
        print("✅ All examples completed successfully!")
        print("="*60)
        
    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Error: {type(e).__name__}: {e}")
        print("\nTroubleshooting:")
        print("1. Ensure Temporal is running: temporal server start-dev")
        print("2. Check .env file has OPENROUTER_API_KEY")
        print("3. Verify API key is active on openrouter.ai")
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)