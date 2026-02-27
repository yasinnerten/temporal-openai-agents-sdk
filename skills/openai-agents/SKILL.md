---
name: openai-agents
description: Complete guide for integrating OpenAI Agents SDK with Temporal workflows, including setup, best practices, and error handling.
license: Apache-2.0
metadata:
  category: ai-integration
  tags: [openai, agents, python, temporal]
---

# OpenAI Agents Integration

This skill provides comprehensive guidance for integrating OpenAI Agents SDK with Temporal workflow orchestration.

## Overview

OpenAI Agents SDK allows building autonomous AI systems that can use tools, make decisions, and execute complex tasks. When combined with Temporal, you get durable, reliable execution with built-in retries and observability.

## Setup and Configuration

### 1. Installation
```bash
# Install OpenAI SDK
pip install openai

# Install with Temporal
pip install temporalio

# Create requirements.txt
cat > requirements.txt << EOF
openai>=1.0.0
temporalio>=1.0.0
python-dotenv>=1.0.0
EOF

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Variables
```python
# .env file
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_MODEL=gpt-4.7
OPENAI_MAX_TOKENS=4096
OPENAI_TEMPERATURE=0.7
TEMPORAL_HOST=localhost:7233
TEMPORAL_NAMESPACE=default
TEMPORAL_TASK_QUEUE=openai-queue
```

### 3. Initialization
```python
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = AsyncOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    organization=os.getenv("OPENAI_ORG_ID", None)
)

model = os.getenv("OPENAI_MODEL", "gpt-4")
```

## Basic Usage

### Chat Completions
```python
@activity.defn
async def chat_completion(prompt: str, system_message: str | None = None) -> str:
    """Generate text using OpenAI chat completion."""
    messages = []

    if system_message:
        messages.append({"role": "system", "content": system_message})

    messages.append({"role": "user", "content": prompt})

    response = await client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        max_tokens=1000,
        temperature=0.7
    )

    return response.choices[0].message.content
```

### Streaming Responses
```python
@activity.defn
async def stream_completion(prompt: str) -> str:
    """Stream OpenAI responses for real-time feedback."""
    full_response = ""

    stream = await client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )

    async for chunk in stream:
        if chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            full_response += content
            # Send progress update
            activity.heartbeat(f"Generated: {len(full_response)} chars")

    return full_response
```

## Agents with Tools

### 1. Function Calling
```python
from typing import TypedDict

class FunctionCall(TypedDict):
    name: str
    arguments: dict

functions = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name or coordinates"
                    }
                },
                "required": ["location"]
            }
        }
    }
]

@activity.defn
async def agent_with_functions(prompt: str) -> str:
    response = await client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        tools=functions,
        tool_choice="auto"
    )

    if response.choices[0].message.tool_calls:
        for tool_call in response.choices[0].message.tool_calls:
            if tool_call.function.name == "get_weather":
                args = json.loads(tool_call.function.arguments)
                weather = await get_weather(args["location"])

                # Send result back to agent
                response = await client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "user", "content": prompt},
                        response.choices[0].message,
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": json.dumps(weather)
                        }
                    ]
                )

    return response.choices[0].message.content
```

### 2. Autonomous Agent Workflow
```python
@workflow.defn
class AgentWorkflow:
    @workflow.run
    async def run(self, task: str, max_steps: int = 5) -> str:
        """Execute autonomous agent with multi-step reasoning."""
        messages = [{"role": "system", "content": "You are a helpful assistant."}]
        messages.append({"role": "user", "content": task})

        for step in range(max_steps):
            response = await workflow.execute_activity(
                agent_step,
                messages,
                task_queue="agent-tasks"
            )

            messages.append(response)

            # Check if task is complete
            if "complete" in response.lower():
                break

            # Check if more tools are needed
            if response.tool_calls:
                tool_results = await workflow.execute_activity(
                    execute_tools,
                    response.tool_calls,
                    task_queue="agent-tasks"
                )

                for tool_id, result in tool_results.items():
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_id,
                        "content": json.dumps(result)
                    })

        return messages[-1]["content"]
```

## Error Handling

### Rate Limiting
```python
import asyncio
from openai import RateLimitError

@activity.defn(
    retry_policy=RetryPolicy(
        maximum_attempts=5,
        initial_interval=timedelta(seconds=2),
        backoff_coefficient=2.0
    )
)
async def rate_limited_call(prompt: str) -> str:
    """Handle OpenAI rate limits gracefully."""
    max_retries = 5
    base_delay = 2.0

    for attempt in range(max_retries):
        try:
            response = await client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except RateLimitError as e:
            if attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)
                print(f"Rate limited, waiting {delay}s...")
                await asyncio.sleep(delay)
            else:
                raise
```

### Token Management
```python
@activity.defn
async def estimate_and_generate(prompt: str) -> dict:
    """Estimate tokens before generation."""
    # Estimate token count (rough approximation)
    estimated_tokens = len(prompt.split()) * 0.75

    max_tokens = 4096
    if estimated_tokens > max_tokens:
        raise ValueError(
            f"Prompt too long: {estimated_tokens} tokens > {max_tokens}"
        )

    response = await client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens
    )

    return {
        "content": response.choices[0].message.content,
        "tokens_used": response.usage.total_tokens,
        "tokens_remaining": max_tokens - response.usage.total_tokens
    }
```

## Integration with Temporal

### 1. Activity Definition
```python
from datetime import timedelta
from temporalio import workflow, activity

@activity.defn(
    start_to_close_timeout=timedelta(seconds=30),
    heartbeat_timeout=timedelta(seconds=5)
)
async def openai_chat_completion(prompt: str, model: str = "gpt-4") -> str:
    """Activity that wraps OpenAI chat completion."""
    response = await client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2000
    )

    return response.choices[0].message.content
```

### 2. Workflow Integration
```python
@workflow.defn
class AIWorkflow:
    @workflow.run
    async def run(self, prompts: list[str]) -> list[str]:
        """Orchestrate multiple OpenAI calls in a workflow."""
        results = []

        for prompt in prompts:
            result = await workflow.execute_activity(
                openai_chat_completion,
                prompt,
                task_queue="ai-tasks"
            )
            results.append(result)

        return results
```

### 3. Worker Configuration
```python
import asyncio
from temporalio.client import Client
from temporalio.worker import Worker

async def main():
    client = await Client.connect(
        "localhost:7233",
        namespace="default"
    )

    worker = Worker(
        client=client,
        task_queue="ai-tasks",
        workflows=[AIWorkflow, AgentWorkflow],
        activities=[openai_chat_completion, agent_step, execute_tools],
        max_concurrent_activity_execution_size=10
    )

    print("Worker started, waiting for tasks...")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
```

## Best Practices

### 1. Cost Optimization
```python
@activity.defn
async def cost_aware_generation(prompt: str, budget: float = 0.10) -> str:
    """Generate text within budget constraints."""
    max_cost_per_call = 0.10

    # Estimate cost (gpt-4: ~$0.03/1K tokens)
    estimated_tokens = len(prompt.split()) * 0.75
    estimated_cost = (estimated_tokens / 1000) * 0.03

    if estimated_cost > max_cost_per_call:
        raise ValueError(f"Cost exceeds budget: ${estimated_cost:.4f}")

    response = await client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=int((max_cost_per_call / 0.03) * 1000)
    )

    return response.choices[0].message.content
```

### 2. Prompt Engineering
```python
@activity.defn
async def structured_generation(prompt: str, schema: dict) -> dict:
    """Generate structured output using prompt engineering."""
    system_prompt = f"""
    You are a structured data generator. Output must match this schema:
    {json.dumps(schema, indent=2)}

    Rules:
    - Output only valid JSON
    - Do not include any text outside JSON
    - Follow schema types exactly
    """

    response = await client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3  # Lower temperature for more deterministic output
    )

    return json.loads(response.choices[0].message.content)
```

### 3. Context Management
```python
@workflow.defn
class ContextAwareWorkflow:
    @workflow.run
    async def run(self, initial_prompt: str) -> str:
        """Manage conversation context across turns."""
        context_limit = 8000  # Keep under token limit
        messages = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]

        while True:
            response = await workflow.execute_activity(
                openai_chat_completion,
                json.dumps(messages[-5:]),  # Last 5 messages
                task_queue="context-aware-tasks"
            )

            messages.append({"role": "assistant", "content": response})

            # Check if context limit reached
            total_tokens = sum(len(m["content"].split()) for m in messages)
            if total_tokens > context_limit:
                messages = [
                    {"role": "system", "content": "Context reset. Summarize previous discussion."},
                    {"role": "user", "content": initial_prompt}
                ]

        return response
```

## Testing

### 1. Mocking OpenAI
```python
from unittest.mock import AsyncMock, patch
import pytest

@pytest.mark.asyncio
async def test_openai_activity():
    with patch('openai.AsyncOpenAI.chat.completions.create') as mock:
        mock.return_value = AsyncMock(
            choices=[AsyncMock(
                message=AsyncMock(content="mocked response")
            )]
        )

        result = await openai_chat_completion("test prompt")
        assert result == "mocked response"
```

### 2. Integration Test
```python
from temporalio.testing import WorkflowEnvironment

@pytest.mark.asyncio
async def test_ai_workflow_integration():
    async with WorkflowEnvironment() as env:
        client = await env.client()

        # Mock the activity
        env.mock_activity(
            "openai_chat_completion",
            lambda: "mocked response"
        )

        result = await client.execute_workflow(
            AIWorkflow.run,
            ["prompt1", "prompt2"],
            id="test-1"
        )

        assert result == ["mocked response", "mocked response"]
```

## Monitoring and Observability

### 1. Usage Tracking
```python
from typing import TypedDict

class UsageMetrics(TypedDict):
    total_requests: int
    total_tokens: int
    total_cost: float
    errors: int

metrics = {
    "requests": 0,
    "tokens": 0,
    "cost": 0.0,
    "errors": 0
}

@activity.defn
async def tracked_generation(prompt: str) -> str:
    """Track OpenAI usage metrics."""
    try:
        response = await client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )

        metrics["requests"] += 1
        metrics["tokens"] += response.usage.total_tokens
        metrics["cost"] += response.usage.total_tokens * 0.00003  # gpt-4 pricing

        return response.choices[0].message.content
    except Exception as e:
        metrics["errors"] += 1
        raise
```

### 2. Performance Logging
```python
import time
from datetime import datetime

@activity.defn
async def logged_generation(prompt: str) -> str:
    """Log OpenAI request performance."""
    start_time = time.time()

    response = await client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    duration = time.time() - start_time
    tokens_per_second = response.usage.total_tokens / duration

    # Log to your monitoring system
    print(f"[{datetime.now()}] Request: {tokens_per_second:.2f} tokens/s")

    return response.choices[0].message.content
```

## Security Best Practices

### 1. API Key Management
```python
import os
from dotenv import load_dotenv

load_dotenv()

def get_openai_client():
    """Get configured OpenAI client with proper key management."""
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY not set in environment")

    # Validate key format
    if not api_key.startswith("sk-"):
        raise ValueError("Invalid OpenAI API key format")

    return AsyncOpenAI(api_key=api_key)
```

### 2. Input Sanitization
```python
import re

@activity.defn
async def sanitized_generation(prompt: str) -> str:
    """Generate text with sanitized inputs."""
    # Remove potential prompt injection patterns
    sanitized = re.sub(r'<\|.*?\|>', '', prompt)

    # Limit prompt length
    max_length = 4000
    sanitized = sanitized[:max_length]

    response = await client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": sanitized}]
    )

    return response.choices[0].message.content
```

## References
- [OpenAI Documentation](https://platform.openai.com/docs/)
- [OpenAI Python SDK](https://github.com/openai/openai-python)
- [OpenAI Agents Guide](https://platform.openai.com/docs/guides/agents)
- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference/)
