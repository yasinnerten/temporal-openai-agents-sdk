"""
Basic tests for the example workflows.

These tests demonstrate how to test Temporal workflows.
"""

import pytest
from examples.temporal.workflows import GreetingWorkflow, create_greeting
from temporalio.testing import WorkflowEnvironment


@pytest.mark.asyncio
async def test_create_greeting_activity():
    """Test the create_greeting activity."""
    result = await create_greeting("World")
    assert result == "Hello, World!"


@pytest.mark.asyncio
async def test_greeting_workflow():
    """Test the GreetingWorkflow."""
    async with await WorkflowEnvironment.start_time_skipping() as env:
        async with Worker(
            env.client,
            task_queue="test-task-queue",
            workflows=[GreetingWorkflow],
            activities=[create_greeting],
        ):
            result = await env.client.execute_workflow(
                GreetingWorkflow.run,
                "Tester",
                id="test-greeting-workflow",
                task_queue="test-task-queue",
            )
            assert result == "Hello, Tester!"


# Note: Import Worker here to avoid issues if temporalio is not installed
try:
    from temporalio.worker import Worker
except ImportError:
    Worker = None
    pytest.skip("temporalio not installed", allow_module_level=True)
