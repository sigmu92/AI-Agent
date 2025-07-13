import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


def load_client():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    model = "gemini-2.0-flash-001"
    return client, model

def get_inputs():
    inputs = sys.argv
    if len(inputs) != 2:
        print("invalid inputs, please enter a prompt")
        sys.exit(1)
    return inputs[1]

def print_response(response):
    print(response.text)
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


def main():
    client, model = load_client()
    prompt = get_inputs()
    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)])
    ]
    response = client.models.generate_content(model=model, contents=messages)
    print_response(response)



if __name__ == "__main__":
    main()
