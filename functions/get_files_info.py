import os
from google.genai import types


def get_files_info(working_directory, directory = None):

    full_path = os.path.join(working_directory, directory)
    
    if not os.path.isdir(full_path):
        return f'Error: "{directory}" is not a directory'
    elif not working_directory in os.path.abspath(full_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    try:
        dir_items = os.listdir(full_path)
    except :
        return f'Error: Unable to list items in "{directory}"'
    dir_info = []
    for item in dir_items:
        new_path = os.path.join(full_path, item)
        if not (os.path.isfile(new_path) or os.path.isdir(new_path)):
            return f'Error: {new_path} is not a file or directory'
        try:
            item_size = os.path.getsize(new_path)
        except:
            return "Error: Issue using os.path.getsize()"
        try:
            is_dir = os.path.isdir(new_path)
        except:
            return "Error: Issue using os.path.isdir()"
        dir_info.append(f"- {item}: file_size={item_size} bytes, is_dir={is_dir} ")
    return "\n".join(dir_info)

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)