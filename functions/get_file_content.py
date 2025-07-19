import os
from functions.config import MAX_CHAR
from google.genai import types

def get_file_content(working_directory, file_path):

    full_path = os.path.join(working_directory, file_path)
    
    if not working_directory in os.path.abspath(full_path):
        return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
    elif not os.path.isfile(full_path):
        return f'Error: File not found or is not a regular file: {file_path}. Use get_files_info to locate file.'
    
    too_large_message = f'[...File "{file_path}" truncated at 10000 characters]'

    try:

        with open(full_path, "r") as f:
            file_content_string = f.read(MAX_CHAR)
    except:
        return f'Error: Unable read file "{file_path}" using open() and read()'
    if len(file_content_string) == 10000:
        file_content_string += too_large_message
    
    return file_content_string

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Read content of specified file in specified directory, constrained to the working directory and the first {MAX_CHAR} characters of the file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the desired file, relative to the working directory.",
            ),
        },
    ),
)