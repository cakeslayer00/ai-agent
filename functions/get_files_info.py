import os

from .utils import get_target_path, validate_is_dir, NotARelativePathException

def get_files_info(working_directory: str, directory: str = ".") -> str:
    res = f"Result for '{directory}' directory:\n"
    try:
        target_path = get_target_path(working_directory, directory)
        validate_is_dir(target_path)

        list_of_files: str = "\n".join(
            map(
                lambda x: f"  - {x}: file_size={os.path.getsize(os.path.join(target_path, x))} bytes, is_dir={os.path.isdir(os.path.join(target_path, x))}",
                os.listdir(target_path)
                )
        )

        return res + list_of_files
    except NotARelativePathException:
        return res + f'    Error: Cannot list "{directory}" as it is outside the permitted working directory'
    except Exception as e:
        return res + str(e)

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}
