import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    model = "gemini-2.0-flash-001"
    
    inputs = sys.argv
    if len(inputs) != 2:
        print("invalid inputs, please enter a prompt")
        sys.exit(1)
    contents = inputs[1]

    response = client.models.generate_content(model=model, contents=contents)
    print(response.text)
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print("Hello from aiagent!")


if __name__ == "__main__":
    main()
