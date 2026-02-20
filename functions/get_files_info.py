import os

def get_files_info(working_dir,current_dir):

    abs_working_dir = os.path.abspath(working_dir)
    abs_current_dir = os.path.abspath(os.path.join(abs_working_dir ,current_dir))

    # If the current directory is outside the working directory we disallow it.
    if not(os.path.commonpath([abs_working_dir, abs_current_dir]) == abs_working_dir):
        return f'Error: Cannot list "{current_dir}" as it is outside the permitted working directory'
    
    # Check if both the dir's exist
    if not os.path.exists(abs_current_dir):
        return f'Error: "{current_dir}" does not exist'

    if not os.path.isdir(abs_current_dir):
        return f'Error: "{current_dir}" is not a directory'
    
    contents = os.listdir(abs_current_dir)

    files_info = ""

    for content in contents:
        abs_content = os.path.join(abs_current_dir , content)
        content_size = os.path.getsize(abs_content)
        is_dir = os.path.isdir(abs_content)

        files_info += f'-"{content}": file_size="{content_size}" is_dir="{is_dir}" \n'

    return files_info


 
""" 
# Example run of the above function.
print(get_files_info(".","calculator")) 
 """
 