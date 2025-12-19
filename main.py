import os
import argparse
import sys

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

    if not response.usage_metadata:
        raise RuntimeError("no api response")
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count
    print("Response:")
    results_list = []
    if verbose:
        print(f"Prompt tokens: {prompt_tokens}\nResponse tokens: {response_tokens}")
    if response.candidates:
        for candidate in response.candidates:
            function_call_content = candidate.content
            messages.append(function_call_content)

    if not response.function_calls:
        return response.text

    for function_call in response.function_calls:
        result = call_function(function_call, verbose)
        if (
            not result.parts
            or not result.parts[0].function_response
            or not result.parts[0].function_response.response
        ):
            raise RuntimeError(f"Empty function response for {function_call.name}")
        if verbose:
            print(f"-> {result.parts[0].function_response.response}")
        results_list.append(result.parts[0])

    messages.append(types.Content(role="user", parts=results_list))

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

    # initialize the loop
    iteration = 0

    while True:
        iteration += 1
        print(iteration)
        if iteration >= 20:
            print("Max iterations reached")
            sys.exit(1)

        try:
            response = generate_content(client, messages, args.verbose)
            if response:
                print("Final Response:")
                print(response)
                break

        except Exception as errmes:
            return f"Error: {errmes}"

if __name__ == "__main__":
    main()
