---
name: agent-implementation
description: Complete guide for implementing AI agents including architecture patterns, multi-agent systems, tool calling, and memory management.
license: Apache-2.0
metadata:
  category: ai-agents
  tags: [agents, ai, architecture, tools, memory]
---

# Agent Implementation

This skill provides comprehensive guidance for building AI agents, from basic patterns to advanced multi-agent systems.

## Core Concepts

### Agent Architecture
An agent consists of:
- **Reasoning Engine**: LLM for planning and decision making
- **Memory System**: Short-term (context) and long-term storage
- **Tool Registry**: Available functions/APIs
- **Execution Engine**: Runs tools and collects results
- **State Manager**: Tracks agent state across interactions

### Agent Types
1. **Reactive Agents**: Respond to user queries
2. **Proactive Agents**: Initiate actions autonomously
3. **Multi-Agent Systems**: Specialized agents collaborate
4. **Hierarchical Agents**: Manager oversees sub-agents

## Basic Agent Pattern

### 1. Simple Tool-Using Agent
```python
from openai import AsyncOpenAI

class ToolUsingAgent:
    """Simple agent that can call tools."""

    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key)
        self.tools = {
            "search": self.search_web,
            "calculate": self.calculate,
        }

    async def run(self, query: str) -> str:
        # Plan
        plan = await self.plan(query)

        # Execute
        result = await self.execute_plan(plan)

        return result

    async def plan(self, query: str) -> dict:
        """Create execution plan."""
        response = await self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a planning agent. Plan tool usage."},
                {"role": "user", "content": f"Plan how to: {query}"}
            ],
            tools=self.tool_list()
        )

        return self.parse_plan(response)

    async def execute_plan(self, plan: dict) -> str:
        """Execute the plan step by step."""
        results = []

        for step in plan["steps"]:
            tool = step["tool"]
            args = step["arguments"]

            if tool in self.tools:
                result = await self.tools[tool](**args)
                results.append(result)

        return "\n".join(results)

    def search_web(self, query: str) -> str:
        """Search the web for information."""
        # Implement web search
        return f"Search results for: {query}"

    def calculate(self, expression: str) -> float:
        """Evaluate mathematical expression."""
        try:
            return eval(expression)
        except:
            return f"Could not calculate: {expression}"
```

### 2. Stateful Agent
```python
from typing import TypedDict, Optional
from datetime import datetime

class AgentState(TypedDict):
    messages: list
    current_goal: Optional[str]
    plan: Optional[list]
    results: list
    metadata: dict

class StatefulAgent:
    """Agent with persistent state across interactions."""

    def __init__(self):
        self.state = AgentState(
            messages=[],
            current_goal=None,
            plan=None,
            results=[],
            metadata={"created_at": datetime.now().isoformat()}
        )

    async def process(self, user_input: str) -> str:
        """Process user input with state management."""
        self.state["messages"].append({"role": "user", "content": user_input})

        # Analyze goal
        if not self.state["current_goal"]:
            self.state["current_goal"] = await self.extract_goal(user_input)

        # Update plan if needed
        if not self.state["plan"]:
            self.state["plan"] = await self.create_plan()

        # Execute actions
        result = await self.execute_actions()

        self.state["results"].append(result)

        # Update state
        self.state["messages"].append({"role": "assistant", "content": result})
        return result

    async def extract_goal(self, input: str) -> str:
        """Extract the main goal from user input."""
        # Use LLM to extract goal
        response = await self.client.chat.completions.create(
            model="gpt-4",
            messages=self.state["messages"],
            instructions="Extract the main goal from the user's request."
        )

        return response.choices[0].message.content

    async def create_plan(self) -> list:
        """Create a plan to achieve current goal."""
        response = await self.client.chat.completions.create(
            model="gpt-4",
            messages=self.state["messages"],
            instructions="Create a step-by-step plan to achieve the goal."
        )

        return self.parse_plan(response)

    async def execute_actions(self) -> str:
        """Execute actions from the plan."""
        # Implement action execution
        pass

    def get_state(self) -> AgentState:
        """Get current agent state."""
        return self.state
```

## Multi-Agent Systems

### 1. Specialized Agents
```python
from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseAgent(ABC):
    """Base class for specialized agents."""

    @abstractmethod
    async def process(self, input_data: Any) -> Dict[str, Any]:
        """Process input and return results."""
        pass

class CodeAgent(BaseAgent):
    """Specialized agent for code-related tasks."""

    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        if "code" in input_data:
            return {"code_analysis": self.analyze_code(input_data["code"])}
        else:
            return {"status": "Unknown task type"}

    def analyze_code(self, code: str) -> str:
        """Analyze code quality and issues."""
        return f"Code analysis for: {code}"

class ResearchAgent(BaseAgent):
    """Specialized agent for research tasks."""

    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        if "query" in input_data:
            return {"research": await self.search(input_data["query"])}
        else:
            return {"status": "Unknown task type"}

    async def search(self, query: str) -> str:
        """Search for information."""
        return f"Research results for: {query}"
```

### 2. Agent Orchestrator
```python
from typing import List, Dict, Any
from datetime import datetime

class AgentOrchestrator:
    """Orchestrate multiple specialized agents."""

    def __init__(self, agents: List[BaseAgent]):
        self.agents = agents
        self.history = []

    async def process(self, user_input: str) -> Dict[str, Any]:
        """Route task to appropriate agent and combine results."""
        # Analyze task
        task_type = await self.classify_task(user_input)

        # Select agents
        selected_agents = self.select_agents(task_type)

        # Execute in parallel
        results = await self.execute_parallel(selected_agents, user_input)

        # Aggregate results
        combined = self.combine_results(results)

        # Log history
        self.history.append({
            "timestamp": datetime.now().isoformat(),
            "input": user_input,
            "task_type": task_type,
            "agents": selected_agents,
            "results": combined
        })

        return combined

    async def classify_task(self, user_input: str) -> str:
        """Classify the type of task."""
        classification = await self.llm_classify(user_input)
        return classification

    def select_agents(self, task_type: str) -> List[BaseAgent]:
        """Select agents based on task type."""
        if task_type == "code":
            return [self.agents[0]]  # CodeAgent
        elif task_type == "research":
            return [self.agents[1]]  # ResearchAgent
        return []

    async def execute_parallel(self, agents: List[BaseAgent], input_data: str) -> List[Dict]:
        """Execute agents in parallel."""
        import asyncio
        tasks = [agent.process(input_data) for agent in agents]
        return await asyncio.gather(*tasks)

    def combine_results(self, results: List[Dict]) -> Dict[str, Any]:
        """Combine results from multiple agents."""
        combined = {}
        for result in results:
            combined.update(result)
        return combined
```

## Tool Calling

### 1. Function Definition
```python
from typing import TypedDict, List
from datetime import datetime

class Tool(TypedDict):
    name: str
    description: str
    parameters: dict

# Define available tools
tools = [
    Tool(
        name="search_web",
        description="Search the web for information",
        parameters={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query"
                }
            },
            "required": ["query"]
        }
    ),
    Tool(
        name="calculate",
        description="Perform mathematical calculations",
        parameters={
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Mathematical expression"
                }
            },
            "required": ["expression"]
        }
    ),
]
```

### 2. Tool Execution
```python
import asyncio
import aiohttp

class ToolExecutor:
    """Execute tools and handle results."""

    async def execute(self, tool_name: str, parameters: dict) -> Any:
        """Execute a tool by name with parameters."""
        if tool_name == "search_web":
            return await self.search_web(parameters["query"])
        elif tool_name == "calculate":
            return await self.calculate(parameters["expression"])
        else:
            raise ValueError(f"Unknown tool: {tool_name}")

    async def search_web(self, query: str) -> dict:
        """Search the web using an API."""
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.example.com/search?q={query}") as response:
                data = await response.json()
                return {"results": data.get("results", [])}

    def calculate(self, expression: str) -> float:
        """Calculate mathematical expression safely."""
        try:
            return eval(expression)
        except Exception as e:
            raise ValueError(f"Calculation error: {e}")
```

### 3. Tool Selection
```python
from typing import List, Optional

class ToolSelector:
    """Select and execute appropriate tools based on task."""

    def __init__(self, available_tools: List[Tool]):
        self.tools = {tool["name"]: tool for tool in available_tools}

    async def select_and_execute(self, task: str) -> Any:
        """Select best tool for task and execute."""
        # Use LLM to select tool
        selected_tool = await self.llm_select_tool(task)

        if not selected_tool:
            return {"error": "No suitable tool found"}

        # Get parameters
        parameters = await self.extract_parameters(task, selected_tool)

        # Execute tool
        result = await self.execute_tool(selected_tool.name, parameters)

        return {"tool": selected_tool.name, "result": result}

    async def llm_select_tool(self, task: str) -> Optional[Tool]:
        """Use LLM to select appropriate tool."""
        prompt = f"""
        Given the task: "{task}"
        Available tools: {list(self.tools.keys())}
        Select the best tool and return its name.
        """
        # Call LLM
        # response = await self.client.chat.completions.create(...)
        # return response.choices[0].message.content
        return None

    async def extract_parameters(self, task: str, tool: Tool) -> dict:
        """Extract parameters from task for the tool."""
        # Use LLM to parse parameters
        return {"query": task}
```

## Memory Systems

### 1. Short-Term Memory
```python
from typing import List, Dict
from collections import deque

class ShortTermMemory:
    """Maintain conversation context with limited window."""

    def __init__(self, max_tokens: int = 4000):
        self.max_tokens = max_tokens
        self.messages: deque(maxlen=100)  # Keep last 100 messages
        self.token_count = 0

    def add(self, role: str, content: str) -> None:
        """Add message to memory."""
        tokens = len(content.split()) * 0.75

        if self.token_count + tokens > self.max_tokens:
            # Prune old messages
            while self.token_count + tokens > self.max_tokens:
                oldest = self.messages.popleft()
                self.token_count -= len(oldest["content"].split()) * 0.75

        self.messages.append({"role": role, "content": content})
        self.token_count += tokens

    def get_context(self) -> List[Dict]:
        """Get current context as list of messages."""
        return list(self.messages)

    def clear(self) -> None:
        """Clear all memory."""
        self.messages.clear()
        self.token_count = 0
```

### 2. Long-Term Memory (Vector Store)
```python
import numpy as np
from typing import List

class VectorStore:
    """Store and retrieve information using vector embeddings."""

    def __init__(self, dimension: int = 1536):
        self.dimension = dimension
        self.documents = []  # List of (embedding, metadata)

    def add(self, text: str, metadata: dict) -> None:
        """Add document to vector store."""
        # Generate embedding
        embedding = self.generate_embedding(text)

        # Store with metadata
        self.documents.append((embedding, metadata))

    def generate_embedding(self, text: str) -> np.ndarray:
        """Generate embedding for text (simplified)."""
        # In real implementation, use OpenAI or other embedding API
        return np.random.rand(self.dimension)  # Placeholder

    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Search for similar documents."""
        query_embedding = self.generate_embedding(query)

        similarities = []
        for doc_embedding, metadata in self.documents:
            # Calculate cosine similarity
            similarity = np.dot(query_embedding, doc_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(doc_embedding)
            )
            similarities.append((similarity, metadata))

        # Return top k
        similarities.sort(key=lambda x: x[0], reverse=True)
        return [metadata for _, metadata in similarities[:top_k]]
```

### 3. Hybrid Memory
```python
from typing import Optional, Dict

class HybridMemory:
    """Combine short-term and long-term memory."""

    def __init__(self):
        self.short_term = ShortTermMemory(max_tokens=4000)
        self.long_term = VectorStore()

    async def retrieve(self, query: str) -> List[Dict]:
        """Retrieve relevant context from both memory systems."""
        # Search short-term
        recent_context = self.short_term.get_context()

        # Search long-term
        relevant_docs = self.long_term.search(query, top_k=3)

        # Combine results
        return {
            "recent": recent_context,
            "documents": relevant_docs
        }
```

## Error Handling

### 1. Retry with Exponential Backoff
```python
import asyncio
import random
from datetime import timedelta

class RetryHandler:
    """Handle retries with exponential backoff."""

    def __init__(self, max_attempts: int = 3):
        self.max_attempts = max_attempts
        self.base_delay = 1.0

    async def execute_with_retry(self, func, *args, **kwargs) -> Any:
        """Execute function with retry logic."""
        for attempt in range(1, self.max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                if attempt == self.max_attempts:
                    raise

                # Exponential backoff
                delay = self.base_delay * (2 ** (attempt - 1))
                jitter = random.uniform(0.8, 1.2)
                await asyncio.sleep(delay * jitter)

                print(f"Retry {attempt}/{self.max_attempts} for {func.__name__}")
```

### 2. Fallback Mechanisms
```python
from typing import Optional

class FallbackAgent:
    """Agent with fallback capabilities."""

    def __init__(self, primary_model: str, fallback_model: str):
        self.primary_model = primary_model
        self.fallback_model = fallback_model

    async def call_llm(self, prompt: str, model: Optional[str] = None) -> str:
        """Call LLM with fallback support."""
        models = [model or self.primary_model, self.fallback_model]

        for model in models:
            try:
                response = await self.client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.choices[0].message.content
            except Exception as e:
                print(f"Model {model} failed: {e}")
                continue

        raise Exception("All models failed")
```

## Monitoring and Observability

### 1. Logging
```python
import logging
from datetime import datetime
from typing import Any

class AgentLogger:
    """Structured logging for agent operations."""

    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

    def log_thought(self, thought: str) -> None:
        """Log agent's reasoning."""
        self.logger.info(f"[THOUGHT] {thought}")

    def log_action(self, action: str, details: Any = None) -> None:
        """Log agent's action."""
        self.logger.info(f"[ACTION] {action}", extra={"details": details})

    def log_result(self, result: str, metric: str) -> None:
        """Log agent's result."""
        self.logger.info(f"[RESULT] {result} ({metric})")

    def log_error(self, error: str, details: Any = None) -> None:
        """Log agent's error."""
        self.logger.error(f"[ERROR] {error}", extra={"details": details})

# Usage
logger = AgentLogger("my_agent")
logger.log_thought("I should search for information")
logger.log_action("Executing web search", {"query": "test"})
logger.log_result("Found 5 results", "search_results: 5")
logger.log_error("API rate limit exceeded", {"limit": 100})
```

### 2. Metrics Collection
```python
from typing import Dict
from collections import defaultdict
from datetime import datetime

class MetricsCollector:
    """Collect and track agent metrics."""

    def __init__(self):
        self.metrics = defaultdict(int)
        self.start_time = datetime.now()

    def record_tool_call(self, tool_name: str, duration: float) -> None:
        """Record tool execution."""
        self.metrics[f"{tool_name}_calls"] += 1
        self.metrics[f"{tool_name}_duration"] += duration

    def record_llm_call(self, model: str, tokens_used: int) -> None:
        """Record LLM usage."""
        self.metrics[f"{model}_calls"] += 1
        self.metrics[f"{model}_tokens"] += tokens_used

    def record_error(self, error_type: str) -> None:
        """Record errors."""
        self.metrics[f"error_{error_type}"] += 1

    def get_metrics(self) -> Dict[str, int]:
        """Get collected metrics."""
        uptime = (datetime.now() - self.start_time).total_seconds()
        return dict(self.metrics)
```

### 3. Tracing
```python
from typing import Optional

class Tracing:
    """Track agent execution flow."""

    def __init__(self):
        self.trace_id = None
        self.spans = []

    def start_span(self, name: str) -> str:
        """Start a new trace span."""
        span_id = f"span_{len(self.spans)}"
        self.spans.append({
            "id": span_id,
            "name": name,
            "start_time": datetime.now().isoformat(),
            "parent": self.trace_id
        })
        return span_id

    def end_span(self, span_id: str, result: Optional[str] = None) -> None:
        """End a trace span."""
        for span in self.spans:
            if span["id"] == span_id:
                span["end_time"] = datetime.now().isoformat()
                span["result"] = result
                break
```

## Temporal Integration

### 1. Workflow Activities
```python
from datetime import timedelta
from temporalio import activity, workflow

@activity.defn
async def agent_thinking(activity_input: dict) -> dict:
    """Activity for agent reasoning/thinking."""
    # Process thinking steps
    reasoning = activity_input.get("reasoning", [])

    # Use LLM for planning
    plan = await create_plan_with_llm(reasoning)

    return {"plan": plan, "reasoning": reasoning}

@workflow.defn
class AgentWorkflow:
    @workflow.run
    async def run(self, task: str) -> dict:
        """Orchestrate agent execution."""
        # Agent thinking
        thinking_result = await workflow.execute_activity(
            agent_thinking,
            {"task": task},
            task_queue="agent-orchestration"
        )

        # Execute plan
        execution_result = await workflow.execute_activity(
            execute_agent_plan,
            {"plan": thinking_result["plan"]},
            task_queue="agent-orchestration"
        )

        return {
            "task": task,
            "plan": thinking_result["plan"],
            "execution": execution_result
        }
```

### 2. Durable Execution
```python
@activity.defn(
    start_to_close_timeout=timedelta(minutes=5),
    heartbeat_timeout=timedelta(seconds=30)
)
async def long_running_agent_task(config: dict) -> dict:
    """Execute long-running agent task with durability."""
    # Send heartbeats
    activity.heartbeat(f"Processing: {config['step']}")

    # Execute work
    result = await process_agent_work(config)

    return {"status": "completed", "result": result}
```

## Best Practices

### 1. Design Patterns
- **Modularity**: Separate concerns (reasoning, execution, memory)
- **Extensibility**: Easy to add new tools and agents
- **Observability**: Comprehensive logging and metrics
- **Testability**: Each component testable independently

### 2. Error Handling
- Always handle API rate limits
- Implement retry with exponential backoff
- Provide fallback mechanisms
- Log all errors with context

### 3. Performance
- Use async/await for I/O operations
- Implement caching for expensive operations
- Use connection pooling for external APIs
- Limit context window to manage tokens

### 4. Security
- Validate all inputs
- Sanitize user prompts
- Manage secrets securely
- Implement rate limiting

## Testing

### 1. Unit Tests
```python
import pytest
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_tool_execution():
    with patch('agent.ToolExecutor.execute') as mock:
        mock.return_value = {"result": "test"}
        executor = ToolExecutor()
        result = await executor.execute("search", {"query": "test"})
        assert result == {"result": "test"}
```

### 2. Integration Tests
```python
from temporalio.testing import WorkflowEnvironment

@pytest.mark.asyncio
async def test_agent_workflow():
    async with WorkflowEnvironment() as env:
        client = await env.client()

        # Mock LLM calls
        env.mock_activity("llm_generate", lambda: "plan")

        # Execute workflow
        result = await client.execute_workflow(
            AgentWorkflow.run,
            "test task",
            id="test-agent-1"
        )

        assert result["status"] == "completed"
```

## References
- [OpenAI Agents Guide](https://platform.openai.com/docs/guides/agents/)
- [LangChain Documentation](https://python.langchain.com/)
- [Temporal Documentation](https://docs.temporal.io/)
- [AutoGPT](https://github.com/microsoft/autogen)
