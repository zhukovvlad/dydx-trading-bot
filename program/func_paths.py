import os


def get_file_path(file_name):
    current_file_path = os.path.abspath(__file__)

    # Get the directory of the current script file
    current_folder_path = os.path.dirname(current_file_path)

    return os.path.join(current_folder_path, file_name)
