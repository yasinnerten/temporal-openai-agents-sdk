# OpenAI SDK Examples

Examples demonstrating the OpenAI Python SDK capabilities.

## Files

- `basic_agent.py` - Simple chat completion example
- `function_calling.py` - Example of using OpenAI function calling

## Setup

1. Copy `.env.example` to `.env` in the root directory:
   ```bash
   cp ../../.env.example ../../.env
   ```

2. Add your OpenAI API key to the `.env` file:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Running the Examples

```bash
# Basic chat completion
python basic_agent.py

# Function calling example
python function_calling.py
```

## What You'll Learn

- How to use the OpenAI chat completions API
- How to implement function calling with OpenAI
- How to handle multi-turn conversations
- Best practices for prompt engineering
