import os
import argparse

from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from functions.call_function import call_function


model = "gemini-2.5-flash"
available_functions = types.Tool(
        function_declarations=[schema_get_files_info,
        schema_get_file_content, schema_write_file,
        schema_run_python_file]
)

def generate_content(client, messages, verbose):

    response = client.models.generate_content(
            model=model, contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt),
    )

    if response.usage_metadata == None:
        raise RuntimeError("no api response")
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count
    print("Response:")
    results_list = []
    if verbose:
        print(f"Prompt tokens: {prompt_tokens}\nResponse tokens: {response_tokens}")
    if response.function_calls:
        for call in response.function_calls:
            print(f"Calling function: {call.name}({call.args})")
            function_result = call_function(call)
            if not function_result.parts[0].function_response.response:
                raise Exception("fatal function didn't return")
            results_list.append(function_result.parts[0])
            if verbose:
                print(f"-> {function_result.parts[0].function_response.response}")
    else:
        print(response.text)


def main():

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise RuntimeError("no api key found")

    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()
    # Now we can access `args.user_prompt`

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")

    generate_content(client, messages, args.verbose)

if __name__ == "__main__":
    main()
