"""
Integration workflow combining Temporal and OpenAI.

This example demonstrates how to use OpenAI within Temporal workflows.
"""

from datetime import timedelta
from temporalio import workflow, activity
from temporalio.common import RetryPolicy
from openai import OpenAI
import os


@activity.defn
async def generate_text_with_openai(prompt: str) -> str:
    """Activity that uses OpenAI to generate text."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")

    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=150,
    )

    return response.choices[0].message.content


@activity.defn
async def process_response(response: str) -> dict:
    """Activity that processes the OpenAI response."""
    return {
        "original_response": response,
        "length": len(response),
        "word_count": len(response.split()),
    }


@workflow.defn
class AIContentWorkflow:
    """Workflow that generates and processes AI content."""

    @workflow.run
    async def run(self, prompt: str) -> dict:
        """Run the AI content workflow."""
        # Generate text using OpenAI
        ai_response = await workflow.execute_activity(
            generate_text_with_openai,
            prompt,
            start_to_close_timeout=timedelta(seconds=30),
            retry_policy=RetryPolicy(
                maximum_attempts=3,
            ),
        )

        # Process the response
        processed_data = await workflow.execute_activity(
            process_response,
            ai_response,
            start_to_close_timeout=timedelta(seconds=10),
        )

        return processed_data
