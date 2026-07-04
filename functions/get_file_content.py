from functions.utils import NotARelativePathError, get_target_path, validate_is_file
from config import MAX_CHARS


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        target_path = get_target_path(working_directory, file_path)
        validate_is_file(target_path)

        with open(target_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)

            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

            return file_content_string
    except NotARelativePathError:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    except Exception as e:
        return str(e)


schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Reads file under a specified path relative to the working directory, providing file contents",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path, relative to the working directory",
                },
            },
            "required": ["file_path"]
        },
    },
}
