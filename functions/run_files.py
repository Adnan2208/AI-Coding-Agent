import os
import subprocess


def run_files(working_dir, file_path, timeout=25):
    abs_working_dir = os.path.abspath(working_dir)
    abs_file_path = os.path.abspath(os.path.join(abs_working_dir, file_path))

    if not os.path.exists(abs_working_dir):
        return f'Error: "{working_dir}" does not exist'

    if not os.path.isfile(abs_file_path):
        return f'Error: "{file_path}" is not a file'
    
    if not abs_file_path.endswith(".py"):
        return f'Not a python file'

    if not (os.path.commonpath([abs_working_dir, abs_file_path]) == abs_working_dir):
        return f'Error: Cannot run "{file_path}" as it is outside the permitted working directory'


    try:
        result = subprocess.run(
            ["python3", abs_file_path],
            cwd=abs_working_dir,
            capture_output=True,
            text=True,
            timeout=timeout,
        )

        stdout = result.stdout.strip()
        stderr = result.stderr.strip()

        if (result.returncode == 0):
            if(stdout):
                return stdout
            return f'Successfully ran "{file_path}"'
        
        elif(stderr):
            return stderr
        return f'Error: "uv run {file_path}" failed with exit code {result.returncode}'

    except subprocess.TimeoutExpired:
        return f'Error: "uv run {file_path}" exceeded {timeout} seconds and was terminated'
    except Exception as e:
        return f"Error: {e}"
