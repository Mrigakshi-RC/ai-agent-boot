import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    working_dir_abs= os.path.abspath(working_directory)
    target_dir=os.path.normpath(os.path.join(working_dir_abs, directory))
    # Will be True or False
    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'
    
    try:
        output_lines = []
        with os.scandir(target_dir) as entries:
            for entry in entries:
                name = entry.name
                # Get file stats using entry.stat()
                stat = entry.stat()
                size = stat.st_size
                # Check if it is a directory or a file
                is_dir = entry.is_dir()
                
                # Format the information into the required string format
                # The format is: - name: file_size=size bytes, is_dir=Boolean
                item_string = f"- {name}: file_size={size} bytes, is_dir={is_dir}"
                output_lines.append(item_string)
        
        # Join all lines into a single string with newlines
        return "\n".join(output_lines)
    except FileNotFoundError:
        return f"Error: Directory not found at '{target_dir}'"
    except PermissionError:
        return f"Error: Permission denied for directory '{target_dir}'"
    except OSError as e:
        return f"Error: An OS error occurred - {e}"
    
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)