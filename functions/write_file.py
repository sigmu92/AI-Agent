import os
from google.genai import types

def write_file(working_directory, file_path, content):

    full_path = os.path.join(working_directory, file_path)
    abs_path = os.path.abspath(full_path)
    if not working_directory in abs_path:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    dir_path = os.path.dirname(abs_path)
    
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    try:
        with open(full_path, "w") as f:
            f.write(content)
    except:
        f"Error: Unable to write content to {file_path}"
    
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description=f"Write the specified content to a file in specified directory at the specified file path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the desired file, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The desired content to be written to the file",
            ),
        },
    ),
)