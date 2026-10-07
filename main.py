from call_function import available_functions, call_function
from prompts import system_prompt
import os
import argparse
from dotenv import load_dotenv
import json

from openai import OpenAI

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")
if api_key is None:
    raise RuntimeError("api_key not found")

from openai import OpenAI

def main():
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]
    user_prompt = args.user_prompt
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
	tools=available_functions,
        temperature=0,
    )
    message = response.choices[0].message
    for tool_call in message.tool_calls:
        result_message = call_function(tool_call, args.verbose)
        if not result_message["content"]:
            raise Exception("Result content is empty")
        if args.verbose:
            print(f"-> {result_message['content']}")
        return result_message

    if response.usage is None:
        raise RuntimeError("usage property is None")
    elif args.verbose is True:
        print(f"User prompt: {user_prompt}\nPrompt tokens: {response.usage.prompt_tokens}\nResponse tokens: {response.usage.completion_tokens}")
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
