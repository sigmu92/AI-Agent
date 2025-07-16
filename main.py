import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions import *
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file


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

def call_function(function_call_part, verbose = False):
    available_functions = ["get_files_info", "get_file_content", "write_file", "run_python_file"]
    function_name = function_call_part.name
    function_args = function_call_part.args
    if not function_name in available_functions:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    if verbose:
        print(print(f"Calling function: {function_name}({function_args})"))
    else:
        print(print(f"Calling function: {function_name}"))


def main():
    client, model = load_client()
    
    inputs = get_inputs()
    prompt = inputs[1]

    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file
        ]
    )
    
    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)])
    ]
    response = client.models.generate_content(
        model=model,
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))

    if not response.text == None:
        print(response.text)
    function_calls = response.function_calls
    if len(function_calls) > 0:
        for call in function_calls:
            print(f"Calling function: {call.name}({call.args})")
    if len(inputs) == 3 and inputs[2] == "--verbose":
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")




if __name__ == "__main__":
    main()
