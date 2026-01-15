"""
OpenAI function calling example.

This example demonstrates how to use OpenAI's function calling capability.
"""

import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def get_weather(location: str, unit: str = "celsius") -> str:
    """Mock function to get weather information."""
    # In a real application, this would call a weather API
    return json.dumps({
        "location": location,
        "temperature": "22",
        "unit": unit,
        "forecast": "sunny",
    })


def main():
    """Run OpenAI function calling example."""
    # Initialize OpenAI client
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not found in environment variables")
        print("Please copy .env.example to .env and add your API key")
        return

    client = OpenAI(api_key=api_key)

    # Define the function schema
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        },
                        "unit": {
                            "type": "string",
                            "enum": ["celsius", "fahrenheit"],
                        },
                    },
                    "required": ["location"],
                },
            },
        }
    ]

    # First API call
    print("Asking about weather...")
    messages = [
        {"role": "user", "content": "What's the weather like in San Francisco?"}
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    # Check if the model wants to call a function
    if tool_calls:
        # Extend conversation with assistant's reply
        messages.append(response_message)

        # Call the function
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

            print(f"\nFunction called: {function_name}")
            print(f"Arguments: {function_args}")

            if function_name == "get_weather":
                function_response = get_weather(
                    location=function_args.get("location"),
                    unit=function_args.get("unit", "celsius"),
                )

                # Extend conversation with function response
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                })

        # Get final response from the model
        second_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )

        print("\nFinal Response:")
        print(second_response.choices[0].message.content)


if __name__ == "__main__":
    main()
