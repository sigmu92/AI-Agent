import os
import subprocess
from functions.config import MAX_RUNTIME

def run_python_file(working_directory, file_path):

    full_path = os.path.join(working_directory, file_path)
    abs_path = os.path.abspath(full_path)
    if not working_directory in abs_path:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(abs_path):
        return f'Error: File "{file_path}" not found.'
    
    if not file_path[-3:] == ".py":
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        run_capture = subprocess.run(['python', f'{full_path}'], text=True, timeout=MAX_RUNTIME, capture_output=True)
    except Exception as e:
        return f'Error: executing Python file: {e}'
    
    stdout = run_capture.stdout
    stderr = run_capture.stderr
    exit_code = run_capture.returncode

    if stdout == None:
        return "No output produced"
    
    return_string = f"STDOUT: {stdout} STDERR: {stderr}"
    if exit_code != 0:
        return_string += f" Process exited with code {exit_code} "
    
    return return_string
