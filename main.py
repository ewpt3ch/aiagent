import os
import argparse

from dotenv import load_dotenv
from google import genai

model = "gemini-2.5-flash"

def main():
    print("hello ai agent")


    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise RuntimeError("no api key found")

    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()
    # Now we can access `args.user_prompt`

    prompt = args.user_prompt
    response = client.models.generate_content(model=model, contents=prompt)

    if response.usage_metadata == None:
        raise RuntimeError("no api response")
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count
    print(f'Prompt tokens: {prompt_tokens}\nResponse tokens: {response_tokens}')
    print(response.text)

if __name__ == "__main__":
    main()
