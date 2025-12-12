import os
import subprocess


def run_python_file(working_directory, file_path, args=[]):
    try:
        # check file is in path and exists and is a python file
        workdir = os.path.abspath(working_directory)
        filepath = os.path.join(working_directory, file_path)
        filepath = os.path.abspath(filepath)
        if not filepath.startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(filepath):
            return f'Error: File "{file_path}" not found.'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        args = ['python', filepath] + args
        result = subprocess.run(args, cwd=workdir, timeout=30, capture_output=True, text=True)

        returnstr = ''
        if result.returncode != 0:
            returnstr += f'Process exited with code {result.returncode}\n'
        if not result:
            returnstr += 'No output produced'
        if result.stdout:
            returnstr += f'STDOUT:\n{result.stdout}\n'
        if result.stderr:
            returnstr += f'STDERR:\n{result.stderr}\n'
        return returnstr


    except Exception as errmes:
        return f"Error: {errmes}"
