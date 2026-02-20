import os

def get_files_info(working_dir,current_dir):

    abs_working_dir = os.path.abspath(working_dir)
    abs_current_dir = os.path.abspath(current_dir)


    print(abs_working_dir)
    print(abs_current_dir)
    # If the current directory is outside the working directory we disallow it.
    if not(abs_current_dir.startswith(abs_working_dir)):
        return f'Error: Cannot list "{current_dir}" as it is outside the permitted working directory'
    
    contents = os.listdir(abs_current_dir)
    print(contents)
    files_info = ""

    for content in contents:
        abs_content = abs_current_dir + "/" + content
        content_size = os.path.getsize(abs_content)
        is_dir = os.path.isdir(abs_content)

        files_info += f'-"{content}": file_size="{content_size}" is_dir="{is_dir}" \n'

    return files_info


 
""" 
# Example run of the above function.
print(get_files_info(".","calculator")) 
 """
 