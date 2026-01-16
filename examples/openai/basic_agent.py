"""
Basic OpenAI SDK example.

This example demonstrates how to use the OpenAI API for chat completions.
"""

import os
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def generate_text(client: OpenAI, prompt: str, model: str = "gpt-3.5-turbo", max_tokens: int = 150) -> str:
    """Generate text using OpenAI chat completion.

    Args:
        client: OpenAI client instance
        prompt: User prompt to send to the model
        model: OpenAI model to use
        max_tokens: Maximum tokens in response

    Returns:
        Generated text response
    """
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=max_tokens,
    )
    content = response.choices[0].message.content
    return content if content else "No response generated"


def chat_with_history(client: OpenAI, messages: list[ChatCompletionMessageParam], model: str = "gpt-3.5-turbo") -> str:
    """Chat with the model using conversation history.

    Args:
        client: OpenAI client instance
        messages: List of message dictionaries with 'role' and 'content'
        model: OpenAI model to use

    Returns:
        Model's response
    """
    response = client.chat.completions.create(
        model=model,
        messages=messages,
    )
    content = response.choices[0].message.content
    return content if content else "No response generated"


def main():
    """Run a basic OpenAI chat completion with multiple examples."""
    # Initialize OpenAI client
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not found in environment variables")
        print("Please copy .env.example to .env and add your API key")
        return

    client = OpenAI(api_key=api_key)

    print("=" * 60)
    print("Example 1: Simple text generation")
    print("=" * 60)
    print("Sending request to OpenAI...")
    response = generate_text(
        client,
        "Explain what Temporal workflow orchestration is in one sentence.",
        max_tokens=100
    )
    print("\nOpenAI Response:")
    print(response)

    print("\n" + "=" * 60)
    print("Example 2: Chat with conversation history")
    print("=" * 60)
    messages: list[ChatCompletionMessageParam] = [
        {"role": "system", "content": "You are a technical tutor specialized in Python."},
        {"role": "user", "content": "What is an async function in Python?"},
    ]
    print("Question: What is an async function in Python?")
    first_response = chat_with_history(client, messages)
    print(f"\nAnswer 1: {first_response}")

    # Continue the conversation
    messages.append({"role": "assistant", "content": first_response})
    messages.append({"role": "user", "content": "Can you give me a code example?"})
    print("\nQuestion: Can you give me a code example?")
    second_response = chat_with_history(client, messages)
    print(f"\nAnswer 2: {second_response}")

    print("\n" + "=" * 60)
    print("Example 3: Generating structured output")
    print("=" * 60)
    structured_prompt = (
        "Generate a list of 3 benefits of using Temporal. "
        "Format each benefit as: '1. Benefit name: description'"
    )
    structured_response = generate_text(client, structured_prompt, max_tokens=200)
    print("\nStructured Output:")
    print(structured_response)

    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
