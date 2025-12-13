import os

from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write content to file at file_path, constrained by working_directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="file_path is the file to write to relative to the working directory.",
            ),
            "content":types.Schema(
                type=types.Type.STRING,
                description="content to write to file."
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):

    try:
        #get the full path and check it's in the correct working dir
        filepath = os.path.join(working_directory, file_path)
        filepath = os.path.abspath(filepath)
        if not filepath.startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        #make the dir if it doesn't exist
        filedir = os.path.dirname(filepath)
        os.makedirs(filedir, exist_ok=True)

        with open(filepath, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as errmes:
        return f"Error: {errmes}"
