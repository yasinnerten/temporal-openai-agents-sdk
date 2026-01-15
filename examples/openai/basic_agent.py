"""
Basic OpenAI SDK example.

This example demonstrates how to use the OpenAI API for chat completions.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def main():
    """Run a basic OpenAI chat completion."""
    # Initialize OpenAI client
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not found in environment variables")
        print("Please copy .env.example to .env and add your API key")
        return

    client = OpenAI(api_key=api_key)

    # Create a chat completion
    print("Sending request to OpenAI...")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Explain what Temporal workflow orchestration is in one sentence."},
        ],
        max_tokens=100,
    )

    # Print the response
    print("\nOpenAI Response:")
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
