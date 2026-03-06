import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path, args=None):
    working_dir_abs = os.path.abspath(working_directory)
    absolute_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
    valid_absolute_file_path = (
        os.path.commonpath([working_dir_abs, absolute_file_path]) == working_dir_abs
    )

    if not valid_absolute_file_path:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(absolute_file_path):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    if os.path.splitext(file_path)[1] != ".py":
        return f'Error: "{file_path}" is not a Python file'

    command = ["python", absolute_file_path]
    if args:
        command.extend(args)

    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=30)

        output = ""
        returncode, stdout, stderr = result.returncode, result.stdout, result.stderr
        if result.returncode != 0:
            output += f"Process exited with code {returncode}\n"
        if not stdout and not stderr:
            return "No output produced"
        else:
            if stdout:
                output += f"STDOUT: {stdout}\n"
            if stderr:
                output += f"STDERR: {stderr}"

        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes the file in a specified directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="An array of any additional extension of the executing command",
                items={"type": types.Type.STRING},
            ),
        },
    ),
)
