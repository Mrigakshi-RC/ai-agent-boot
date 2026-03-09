from google.genai import types
from functions import (
    get_files_info,
    get_file_content,
    run_python_file,
    write_file_content,
)

available_functions = types.Tool(
    function_declarations=[
        get_files_info.schema_get_files_info,
        get_file_content.schema_get_file_content,
        run_python_file.schema_run_python_file,
        write_file_content.schema_write_file,
    ],
)


def call_function(function_call, verbose=False):
    function_map = {
        "get_file_content": get_file_content.get_file_content,
        "get_files_info": get_files_info.get_files_info,
        "run_python_file": run_python_file.run_python_file,
        "write_file_content": write_file_content.write_file_content,
    }
    function_name = function_call.name or ""
    print(f"- Calling function: {function_name}")
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    args = dict(function_call.args) if function_call.args else {}
    args["working_directory"]="./calculator"

    function_result=function_map[function_name](**args)
    return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"result": function_result},
        )
    ],
)