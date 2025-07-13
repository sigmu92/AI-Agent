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
    if len(inputs) == 1:
        print("invalid inputs, please enter a prompt")
        sys.exit(1)
    return inputs

def main():
    client, model = load_client()
    inputs = get_inputs()
    prompt = inputs[1]
    
    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)])
    ]
    response = client.models.generate_content(model=model, contents=messages)

    print(response.text)
    if len(inputs) == 3 and inputs[2] == "--verbose":
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")




if __name__ == "__main__":
    main()
