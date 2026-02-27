---
name: temporal-workflows
description: Comprehensive guide for Temporal workflow orchestration patterns including activity design, error handling, and testing strategies.
license: Apache-2.0
metadata:
  category: backend-orchestration
  tags: [temporal, workflow, python, testing]
---

# Temporal Workflow Patterns

This skill provides comprehensive guidance for building robust Temporal workflows with OpenAI agents integration.

## Core Concepts

Temporal is a durable execution platform that orchestrates distributed systems through workflows, activities, and workers.

**Key Terminology:**
- **Workflow**: Definition of how tasks should be executed (idempotent, durable)
- **Activity**: Unit of work that can be retried, timed out, and scheduled
- **Worker**: Long-running process that polls for tasks and executes activities
- **Activity Task**: An instruction to an activity instance with inputs and a result
- **Workflow Execution**: Single run of a workflow with a unique ID

## Workflow Design Principles

### 1. Idempotency
Workflows must be idempotent - running the same workflow multiple times with the same inputs should produce the same result.

```python
@workflow.defn
class ProcessOrderWorkflow:
    @workflow.run
    async def run(self, order_id: str) -> OrderResult:
        # Check if already processed
        existing = await workflow.execute_activity(
            check_order_status,
            order_id,
            task_queue="order-processing"
        )

        if existing.processed:
            return OrderResult(
                status="already_processed",
                order_id=order_id
            )

        # Process the order
        result = await workflow.execute_activity(
            process_order,
            order_id,
            task_queue="order-processing"
        )

        return result
```

### 2. Deterministic Logic
Workflows should not depend on external state or nondeterministic operations.

**Good:**
```python
@workflow.defn
class GenerateReportWorkflow:
    @workflow.run
    async def run(self, date: datetime) -> Report:
        # Use inputs only, not external state
        data = await workflow.execute_activity(
            fetch_data,
            date,
            task_queue="report-generation"
        )
        return data
```

**Bad:**
```python
@workflow.defn
class GenerateReportWorkflow:
    @workflow.run
    async def run(self) -> Report:
        # Reading from global state - nondeterministic
        return global_data_store.get_latest()
```

### 3. Error Handling
Use Temporal's built-in retry mechanisms for transient failures.

```python
@activity.defn
async def call_openai_api(prompt: str) -> str:
    max_attempts = 3
    initial_interval = timedelta(seconds=1)
    backoff_coefficient = 2.0

    for attempt in range(max_attempts):
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except RateLimitError as e:
            if attempt < max_attempts - 1:
                await asyncio.sleep(initial_interval * (backoff_coefficient ** attempt))
                continue
            raise
```

### 4. Signal Handling
Use signals for asynchronous communication and cancellation.

```python
from temporalio import workflow

class ProcessingWorkflow:
    @workflow.run
    async def run(self, data: str) -> None:
        # Set up signal handler
        query_handler = workflow.wait_condition(
            self.processing_query.set,
            timeout=timedelta(hours=24)
        )

        # Start activity
        await workflow.execute_activity(
            long_running_task,
            data,
            task_queue="processing"
        )

        # Wait for query or timeout
        await asyncio.wait([query_handler], return_when=asyncio.FIRST_COMPLETED)
```

## Activity Best Practices

### 1. Heartbeat Activities
For long-running activities, implement heartbeat to avoid worker timeout.

```python
@activity.defn
async def process_large_file(file_path: str) -> ProcessingResult:
    async for progress in generate_progress(file_path):
        # Send heartbeat updates
        activity.heartbeat("Processing: " + progress)
        await asyncio.sleep(5)

    return ProcessingResult(status="completed", file_path=file_path)
```

### 2. Type Safety
Use TypedDict or dataclasses for structured data.

```python
from typing import TypedDict

class OpenAIResponse(TypedDict):
    content: str
    tokens_used: int
    model: str

@activity.defn
async def generate_text(prompt: str) -> OpenAIResponse:
    response = await client.chat.completions.create(...)
    return OpenAIResponse(
        content=response.choices[0].message.content,
        tokens_used=response.usage.total_tokens,
        model="gpt-4"
    )
```

### 3. Caching Strategies
Implement caching for expensive operations.

```python
from functools import lru_cache

@lru_cache(maxsize=100)
@activity.defn
async def get_embedding(text: str) -> list[float]:
    return await openai_client.embeddings.create(text=text)
```

## Retry Policies

### Transient Errors (Retry)
Network timeouts, rate limits, temporary service unavailability.

```python
@activity.defn(
    retry_policy=RetryPolicy(
        maximum_attempts=5,
        initial_interval=timedelta(seconds=1),
        backoff_coefficient=2.0,
        non_retryable_error_types=[ValueError, TypeError]
    )
)
async def transient_operation(input_data: str) -> str:
    return await external_api_call(input_data)
```

### Non-Retryable Errors (No Retry)
Validation errors, permission denied, not found.

```python
@activity.defn(
    retry_policy=RetryPolicy(
        maximum_attempts=1,
        non_retryable_error_types=[ValidationError, PermissionError]
    )
)
async def validate_user(user_id: str) -> User:
    if not user_exists(user_id):
        raise ValidationError("User not found")
    return get_user(user_id)
```

## Testing Strategies

### 1. Unit Testing Activities
```python
import pytest
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_generate_content():
    with patch('openai.OpenAI.chat.completions.create') as mock:
        mock.return_value = Mock(
            choices=[Mock(message=Mock(content="test response"))]
        )

        result = await generate_content("test prompt")
        assert result == "test response"
        mock.assert_called_once()
```

### 2. Workflow Testing
```python
from temporalio.testing import WorkflowEnvironment

@pytest.mark.asyncio
async def test_order_processing_workflow():
    async with WorkflowEnvironment() as env:
        client = await env.client()

        result = await client.execute_workflow(
            ProcessOrderWorkflow.run,
            "order-123",
            id="test-workflow-1"
        )

        assert result.status == "completed"
```

### 3. Integration Testing
```python
@pytest.mark.asyncio
async def test_temporal_openai_integration():
    worker = await Worker(
        client=client,
        task_queue="test-queue",
        activities=[generate_content, analyze_content],
        workflows=[MultiStepAIChainWorkflow],
    )

    # Run worker in background
    import asyncio
    task = asyncio.create_task(worker.run())

    # Execute workflow
    result = await client.execute_workflow(
        MultiStepAIChainWorkflow.run,
        "test topic",
        id="integration-test-1"
    )

    # Cleanup
    task.cancel()
```

## Common Patterns

### 1. Parallel Activity Execution
```python
@workflow.defn
class ParallelProcessingWorkflow:
    @workflow.run
    async def run(self, items: list[str]) -> list[str]:
        # Execute activities in parallel
        results = await asyncio.gather(*[
            workflow.execute_activity(
                process_item,
                item,
                task_queue="processing"
            )
            for item in items
        ])
        return results
```

### 2. Child Workflows
```python
@workflow.defn
class ParentWorkflow:
    @workflow.run
    async def run(self, data: dict) -> dict:
        # Execute child workflow
        child_result = await workflow.execute_child_workflow(
            ChildWorkflow.run,
            data["child_input"],
            id="child-1"
        )
        return {"parent": data, "child": child_result}
```

### 3. Query Methods
```python
@workflow.defn
class QueryableWorkflow:
    @workflow.run
    async def run(self, workflow_id: str) -> None:
        # Set query handler
        await workflow.set_query_handler(self.process_query.set(workflow_id))

        # Execute long-running activity
        await workflow.execute_activity(
            long_task,
            workflow_id,
            task_queue="tasks"
        )

    @workflow.query
    async def process_query(self, query: str) -> str:
        return f"Query result: {query}"
```

## Performance Optimization

### 1. Activity Timeout Tuning
```python
@activity.defn(
    start_to_close_timeout=timedelta(seconds=30)
)
async def optimized_activity(input_data: str) -> str:
    # Processing logic here
    return result
```

### 2. Batch Processing
```python
@workflow.defn
class BatchProcessingWorkflow:
    @workflow.run
    async def run(self, items: list[str]) -> list[dict]:
        batch_size = 10
        results = []

        for i in range(0, len(items), batch_size):
            batch = items[i:i + batch_size]
            batch_result = await workflow.execute_activity(
                process_batch,
                batch,
                task_queue="batch-processing"
            )
            results.extend(batch_result)

        return results
```

## Environment Configuration

### Development
```python
# .env.dev
TEMPORAL_HOST=localhost:7233
TEMPORAL_NAMESPACE=default
OPENAI_API_KEY=sk-test-key
TEMPORAL_TASK_QUEUE=dev-queue
```

### Production
```python
# .env.prod
TEMPORAL_HOST=temporal.prod.example.com:7233
TEMPORAL_NAMESPACE=production
OPENAI_API_KEY=sk-prod-key
TEMPORAL_TASK_QUEUE=prod-queue
TEMPORAL_TLS_ENABLED=true
```

## Debugging Techniques

### 1. Workflow History
```bash
# View workflow execution history
tctl workflow show --workflow-id <workflow-id>

# View activity history
tctl activity show --workflow-id <workflow-id>
```

### 2. Metrics and Observability
```python
from temporalio.contrib.opentelemetry import OpenTelemetryConfig

# Enable metrics tracing
config = OpenTelemetryConfig(
    metrics_exporter="prometheus",
    traces_exporter="jaeger"
)

worker = Worker(
    client=client,
    task_queue="production-queue",
    activities=activities,
    workflows=workflows,
    telemetry_config=config
)
```

### 3. Local Activity Invocation
```python
from temporalio.testing import WorkflowEnvironment

@pytest.mark.asyncio
async def test_workflow_locally():
    async with WorkflowEnvironment() as env:
        # Activities run locally without Temporal server
        client = await env.client()

        result = await client.execute_workflow(
            MyWorkflow.run,
            arg="test",
            id="local-test-1"
        )

        assert result == "expected"
```

## References
- [Temporal Documentation](https://docs.temporal.io/)
- [Temporal Python SDK](https://github.com/temporalio/sdk-python)
- [Temporal Best Practices](https://docs.temporal.io/application-development/monitoring)
- [Temporalio Testing](https://docs.temporal.io/application-development/testing)
