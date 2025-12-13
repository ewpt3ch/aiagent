import os
import config

from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Get the contents of the specified file, constrained to the working_directory and 10k or fewer characters.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="file_path is the file to get the contents of, relative to the working directory.",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    try:
        # create full paths and do checks
        fullpath = os.path.join(working_directory, file_path)
        fullpath = os.path.abspath(fullpath)
        if not fullpath.startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(fullpath):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # read the file
        with open(fullpath, "r") as f:
            file_content = f.read(config.MAX_TOKEN)
            if len(file_content) == 10000:
                file_content += f' [...File "{file_path}" truncated at 10000 characters]'

        return file_content

    except Exception as errmes:
        return f'Error: {errmes}'
