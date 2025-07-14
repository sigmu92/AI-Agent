import os

def write_file(working_directory, file_path, content):

    full_path = os.path.join(working_directory, file_path)
    abs_path = os.path.abspath(full_path)
    if not working_directory in abs_path:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
       
    try:
        with open(full_path, "w") as f:
            f.write(content)
    except:
        f"Error: Unable to write content to {file_path}"
    
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
