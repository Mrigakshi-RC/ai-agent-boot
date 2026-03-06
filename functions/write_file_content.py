import os
from google.genai import types

def write_file_content(working_directory, file_path, content):
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
    valid_target_file = (
        os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
    )

    if not valid_target_file:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if os.path.isdir(target_file):
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    
    try:
        os.makedirs(working_dir_abs, exist_ok=True)
        with open(target_file, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception:
        return ("Error: whatchu doing man")
    
schema_write_file = types.FunctionDeclaration(
    name="write_file_content",
    description="Overwrites the contents of the file in the specified directory with the content that is provided",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content that needs to be overwritten",
            ),
        },
    ),
)