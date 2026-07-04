import subprocess

from functions.utils import get_target_path, validate_is_file,  NotARelativePathException, NotAFileException

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        target_path = get_target_path(working_directory, file_path)
        validate_is_file(target_path)

        if not target_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_path] + args if args else ["python", target_path]

        return run_subprocess(command)
    except NotARelativePathException:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    except NotAFileException:
        return f'Error: "{file_path}" does not exist or is not a regular file'
    except ExecutionException as e:
        return f"Error: executing Python file: {e}"

def run_subprocess(command) -> str:
    output: str = ""
    try:
        completed = subprocess.run(command, capture_output=True, text=True, timeout=30)

        if completed.returncode != 0:
            output += "Process exited with code X\n"
        if not completed.stderr and not completed.stdout:
            output += "No output produced\n"
        output += f"STDOUT: {completed.stdout}\n"
        output += f"STDERR: {completed.stderr}\n"

        return output
    except Exception as e:
        raise ExecutionException(e)

class ExecutionException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs python program under a specified path relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": "string",
                    "description": "List of command arguments to run with",
                },
            },
            "required": ["file_path"]
        },
    },
}
