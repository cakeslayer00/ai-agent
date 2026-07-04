import os

from functions.utils import get_target_path, validate_is_file, NotARelativePathException

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        target_path = get_target_path(working_directory, file_path)

        if os.path.isdir(target_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(target_path), exist_ok=True)

        with open(target_path, "w") as f:
            f.write(content)

            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except NotARelativePathException:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    except Exception as e:
        return str(e)


schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes given text to the file under a specified path relative to the working directory, or creates new file and writes there",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path, relative to the working directory",
                },
                "content": {
                    "type": "string",
                    "description": "Content to write to file, relative to the working directory",
                },
            },
            "required": ["file_path", "content"]
        },
    },
}
