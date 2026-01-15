# OpenRouter Integration for Temporal OpenAI Agents SDK

This folder contains a **complete implementation** using OpenRouter with free DeepSeek R1 model.

## Quick Start

### 1. Get OpenRouter API Key

1. Visit [OpenRouter.ai](https://openrouter.ai/)
2. Sign up for a free account
3. Go to [API Keys](https://openrouter.ai/keys)
4. Create a new API key
5. Copy the key (starts with `sk-or-v1-...`)

### 2. Setup Environment

Copy the `.env.example` to `.env` file in this folder:

```bash
cd open-router
cp .env.example .env
echo "OPENROUTER_API_KEY=sk-or-v1-your-key-here" > .env
```

### 3. Install Dependencies

```bash
# From project root
pip install -r requirements.txt

# Or install in this folder
pip install temporalio openai python-dotenv
```

### 4. Start Temporal Server

```bash
temporal server start-dev
```

### 5. Run the Example

```bash
python example.py
```

## File Structure

```
open-router/
├── README.md           # This file
├── .env               # Your OpenRouter API key (create this)
├── example.py         # Complete working example
├── client.py          # OpenRouter client setup
└── workflows.py       # Sample workflows
```

## Available Models

### Free Models
- `deepseek/deepseek-r1:free` - Free tier (rate limited)

### Premium Models
- `deepseek/deepseek-r1` - Higher limits
- `openai/gpt-4-turbo` - GPT-4 Turbo
- `anthropic/claude-3.5-sonnet` - Claude 3.5
- `google/gemini-pro-1.5` - Gemini Pro

[View all models](https://openrouter.ai/models)

## Usage Examples

### Basic Agent

```python
from workflows import SimpleAgentWorkflow
from client import get_openrouter_client

client = await get_openrouter_client()

handle = await client.start_workflow(
    SimpleAgentWorkflow.run,
    "What is Temporal?",
    id="my-workflow",
    task_queue="openrouter-queue",
)

result = await handle.result()
print(result)
```

### Custom Model

```python
from workflows import create_custom_workflow
from client import get_openrouter_client

# Create workflow with different model
CustomWorkflow = create_custom_workflow(
    model="deepseek/deepseek-r1",  # Premium version
    system_prompt="You are a code expert."
)

client = await get_openrouter_client()
# ... run workflow
```

## Troubleshooting

### "OPENROUTER_API_KEY not found"
- Create `.env` file in `open-router/` folder
- Add: `OPENROUTER_API_KEY=sk-or-v1-...`

### "Failed to connect to Temporal"
- Start server: `temporal server start-dev`

### Authentication errors
- Verify API key is active on [OpenRouter.ai](https://openrouter.ai/keys)
- Ensure key starts with `sk-or-v1-`

### Rate limits
- Free tier has limits
- Upgrade to premium model
- Add delays between requests

## Comparison: OpenAI vs OpenRouter

| Feature | OpenAI (Main) | OpenRouter (This Folder) |
|---------|--------------|--------------------------|
| API Key | `OPENAI_API_KEY` | `OPENROUTER_API_KEY` |
| Free Tier | ❌ No | ✅ Yes (DeepSeek) |
| Models | OpenAI only | Multiple providers |
| Setup | Main project | Separate folder |
| Config | `.env` in root | `.env` in `open-router/` |

## Next Steps

- Try different models
- Build your own workflows
- Compare with main OpenAI implementation
- Deploy to production