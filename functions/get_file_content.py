import os
from config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory, file_path):
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
    valid_target_file = (
        os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
    )

    if not valid_target_file:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    file_content_string=None
    try:
        with open(target_file, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            print(f.read(1))
            # After reading the first MAX_CHARS...
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return file_content_string
    except Exception as e:
        print(e, "is it")
        return ("Error: whatchu doing man")

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Shows the contents of the file in a specified directory, upto the max number of characters specified",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file relative to the working directory",
            ),
        },
    ),
)