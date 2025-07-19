import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.write_file import schema_write_file, write_file
from functions.run_python_file import schema_run_python_file, run_python_file


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

    working_directory = "calculator"
    available_functions = {"get_files_info": get_files_info,
                            "get_file_content":get_file_content,
                            "write_file": write_file,
                            "run_python_file": run_python_file}
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
    function_args['working_directory'] = working_directory
    try:
        output = available_functions[function_name](**function_args)
    except Exception as e:
        return f'Error: Unable to execute {function_name} due to error {e}'

    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f"Calling function: {function_name}")

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": output},
            )
        ],
    )



def main():
    verbose = False
    client, model = load_client()
    
    inputs = get_inputs()
    prompt = inputs[1]
    if len(inputs) == 3 and inputs[2] == "--verbose":
        verbose = True
    
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, execute a function call plan. You can perform the following operations:

    - List contents of files and directories
    - Write to files
    - Run python programs
   
    LOCATE FILES USING THE GET_FILES_INFO SCHEMA.
    
    Use the operations provided to you to address the user's request. Do not make further requests of the user. 
    
    All paths you provide should be relative to the working directory. The working directory may have additional directories that you can access via You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.

    Fix bugs by addressing the logic issues in the code. Do not use print statements to acheive the user's desired output.

    Do not respond with text until you have completed the request or answered the user's question. When you have completed the request or answered the questions, respond with a description of the issue or the answer to the question.
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

    count = 0

    try:
        while count < 20:
  
            response = client.models.generate_content(
                model=model,
                contents=messages,
                config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))

            for candidate in response.candidates:
                messages.append(types.Content(role = candidate.content.role, parts = candidate.content.parts))

            function_call = response.function_calls     
            if response.text != None:
                print(response.text)
                return
            if function_call != None:
                function_response = call_function(function_call[0], verbose)
            else:
                print("Error: No function call requested")
                return

            if function_response.parts[0].function_response.response == None:
                raise "Error: No response from function call"
            
            messages.append(types.Content(role = "tool", parts = function_response.parts))
            count += 1
        
            if verbose:
                print(f"User prompt: {prompt}")
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
                print(f"-> {function_response.parts[0].function_response.response}")    
            
    except Exception as e:
        print(f"Error: Unexpected error {e} occured")
        return

    return response.text
    




if __name__ == "__main__":
    main()
