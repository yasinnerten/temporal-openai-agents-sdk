"""
OpenRouter client configuration for Temporal.
This module handles the connection to OpenRouter API and Temporal server.
"""
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from temporalio.client import Client
from temporalio.contrib.openai_agents import OpenAIAgentsPlugin


# Load environment variables from .env file in this directory
load_dotenv()


async def get_openrouter_client() -> Client:
    """
    Create and return a Temporal client configured with OpenRouter.
    
    This function:
    1. Loads OPENROUTER_API_KEY from .env file
    2. Creates OpenRouter client with OpenAI-compatible interface
    3. Connects to Temporal server with OpenRouter plugin
    
    Returns:
        Client: Configured Temporal client ready to use
        
    Raises:
        ValueError: If OPENROUTER_API_KEY is not set
        Exception: If connection to Temporal fails
    """
    # Get API key from environment
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    if not api_key:
        raise ValueError(
            "OPENROUTER_API_KEY not found in .env file.\n\n"
            "Setup instructions:\n"
            "1. Get free API key: https://openrouter.ai/keys\n"
            "2. Create .env file in open-router/ folder\n"
            "3. Add: OPENROUTER_API_KEY=sk-or-v1-your-key-here"
        )
    
    # Initialize OpenRouter client
    openrouter_client = AsyncOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    
    # Get Temporal address (default to localhost)
    temporal_address = os.getenv("TEMPORAL_ADDRESS", "localhost:7233")
    
    # Connect to Temporal with OpenRouter plugin
    client = await Client.connect(
        temporal_address,
        plugins=[OpenAIAgentsPlugin(client=openrouter_client)]
    )
    
    return client


async def get_openrouter_client_with_custom_model(model: str) -> Client:
    """
    Create Temporal client with a specific OpenRouter model.
    
    Args:
        model: OpenRouter model ID (e.g., "deepseek/deepseek-r1")
        
    Returns:
        Client: Configured Temporal client
    """
    # For now, model is set at workflow level
    # This function exists for future enhancements
    return await get_openrouter_client()