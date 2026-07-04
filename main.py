import os
import sys
import argparse

from openai import OpenAI
from dotenv import load_dotenv
from prompts import system_prompt
from call_function import available_functions, call_function

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

if not api_key:
    raise Exception("No OPENROUTER_API_KEY provided, please add it to .env")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)


def main():
    print("Hello from ai-agent!")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    for _ in range(20):
        response = client.chat.completions.create(
            model = "openrouter/free",
            messages=messages,
            tools=available_functions,
        )

        message = response.choices[0].message
        messages.append(message)

        if message.tool_calls:
            result_message = handle_function_calls(message, args)
            messages.extend(result_message)
        else:
            print_content(response, args)
            return

    print("Reached max iterations (20) without a final answer. Try rephrasing your prompt.")
    sys.exit(1)


def handle_function_calls(message, args):
    results = []
    for tool_call in message.tool_calls:
        result_message = call_function(tool_call, args.verbose)

        if not result_message["content"]:
            result_message["content"] = "(no output)"

        if args.verbose:
            print(f"-> {result_message['content']}")
        results.append(result_message)
    return results

def print_content(response, args) -> None:
    if args.verbose:
        print(f"""User prompt: {args.user_prompt}
Prompt tokens: {response.usage.prompt_tokens}
Response tokens: {response.usage.completion_tokens}
              """)
    print(f"Response: {response.choices[0].message.content}")

if __name__ == "__main__":
    main()
