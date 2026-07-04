import os

def get_target_path(working_directory: str, relative_path: str = ".") -> str:
    """Returns target path relative to this working directory"""
    abs_work_dir = os.path.abspath(working_directory)
    target_path = os.path.join(abs_work_dir, relative_path)
    target_path_normalized = os.path.normpath(target_path)

    if os.path.commonpath([abs_work_dir, target_path_normalized]) != abs_work_dir:
        raise NotARelativePathException("Given path is outside of the working directory")

    return target_path_normalized

def validate_is_dir(directory_path: str) -> None:
    if not os.path.isdir(directory_path):
        raise NotADirectoryException(f'Error: "{directory_path}" is not a directory')

def validate_is_file(file_path: str) -> None:
    if not os.path.isfile(file_path):
        raise NotAFileException(f'Error: File not found or is not a regular file: "{file_path}"')

class NotAFileException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class NotADirectoryException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class NotARelativePathException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
