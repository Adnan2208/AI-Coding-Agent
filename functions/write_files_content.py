import os

def write_files_content(working_dir,file_path,content):
    
    abs_working_dir = os.path.abspath(working_dir)
    abs_file_path = os.path.join(abs_working_dir,file_path)


    if not(os.path.commonpath([abs_working_dir,abs_file_path]) == abs_working_dir):
        return f'"{abs_file_path}" is not a part of the working dir: "{abs_working_dir}"'
    
    # Check if dir and file exists
    if not os.path.exists(abs_working_dir):
        return f'Error: "{working_dir}" does not exist'

    if not os.path.exists(abs_file_path):
        with open(abs_file_path,'x',encoding='utf-8') as f:
            f.write(content)
    else:
        try:
            with open(abs_file_path, 'w' , encoding='utf-8') as file:
                file.write(content)
    
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    
