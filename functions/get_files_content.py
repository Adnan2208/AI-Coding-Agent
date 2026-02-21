import os

def get_files_content(working_dir,file_path):
    
    abs_working_dir = os.path.abspath(working_dir)
    abs_file_path = os.path.join(abs_working_dir,file_path)

    print(abs_working_dir)
    print(abs_file_path)

    if not(os.path.commonpath([abs_working_dir,abs_file_path]) == abs_working_dir):
        return f'"{abs_file_path}" is not a part of the working dir: "{abs_working_dir}"'
    
    # Check if both the dir's exist
    if not os.path.exists(abs_working_dir):
        return f'Error: "{working_dir}" does not exist'

    if not os.path.isdir(abs_file_path):
        return f'Error: "{file_path}" is not a directory'

    try:
        with open(abs_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            print(content)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
