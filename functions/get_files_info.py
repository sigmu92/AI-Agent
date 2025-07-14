import os


def get_files_info(working_directory, directory = None):

    full_path = os.path.join(working_directory, directory)
    
    if not os.path.isdir(full_path):
        return f'Error: "{directory}" is not a directory'
    elif not working_directory in os.path.abspath(full_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    dir_items = os.listdir(full_path)
    dir_info = []
    for item in dir_items:
        new_path = os.path.join(full_path, item)
        if not (os.path.isfile(new_path) or os.path.isdir(new_path)):
            return f'Error: {new_path} is not a file or directory'
        item_size = os.path.getsize(new_path)
        is_dir = os.path.isdir(new_path)
        dir_info.append(f"- {item}: file_size={item_size} bytes, is_dir={is_dir} ")
    return "\n".join(dir_info)