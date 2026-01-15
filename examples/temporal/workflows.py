"""
Basic Temporal workflow example.

This example demonstrates a simple workflow that processes a greeting.
"""

from datetime import timedelta
from temporalio import workflow, activity
from temporalio.common import RetryPolicy


@activity.defn
async def create_greeting(name: str) -> str:
    """Activity that creates a greeting message."""
    return f"Hello, {name}!"


@workflow.defn
class GreetingWorkflow:
    """A simple workflow that greets a person."""

    @workflow.run
    async def run(self, name: str) -> str:
        """Run the workflow."""
        # Execute the activity with a retry policy
        greeting = await workflow.execute_activity(
            create_greeting,
            name,
            start_to_close_timeout=timedelta(seconds=10),
            retry_policy=RetryPolicy(
                maximum_attempts=3,
            ),
        )
        return greeting
