import json
from os import listdir
from os.path import isfile, join, isdir
import chardet
from abc import ABC, abstractmethod


class SerializableToDict(ABC):
    """
    Abstract base class for objects that can be serialized to a dictionary.
    """

    @abstractmethod
    def to_dictionary(self):
        """
        Converts the object to a dictionary representation.

        Returns:
        - dict: Dictionary representation of the object.
        """
        pass


def get_files_recursively(directory, ignore_patterns=None):
    """
    Recursively retrieves all files in a directory and its subdirectories.

    Args:
    - directory (str): Directory path to start exploring.
    - ignore_patterns (list, optional): List of patterns for files to be ignored.

    Returns:
    - list: List of file paths found in the directory and its subdirectories.
    """
    if ignore_patterns is None:
        ignore_patterns = []

    files = []

    for item in listdir(directory):
        item_path = join(directory, item)

        if any(pattern in item_path for pattern in ignore_patterns):
            continue

        if isdir(item_path):
            files.extend(get_files_recursively(item_path, ignore_patterns))
        elif isfile(item_path):
            files.append(item_path)

    return files


def find_files_with_extension(directory, extension):
    """
    Recursively finds all files with a specific extension in a directory and its subdirectories.

    Args:
    - directory (str): Directory path to start exploring.
    - extension (str): Extension of the files to search for (e.g., '.py').

    Returns:
    - list: List of file paths that have the specified extension.
    """
    files = []

    for item in listdir(directory):
        item_path = join(directory, item)
        if isdir(item_path):
            files.extend(find_files_with_extension(item_path, extension))
        elif item.endswith(extension):
            files.append(item_path)

    return files


def read_gitignore_patterns(gitignore_path):
    """
    Reads a .gitignore file and extracts patterns for ignored files.

    Args:
    - gitignore_path (str): Path to the .gitignore file.

    Returns:
    - list: List of patterns for files to be ignored.
    """
    ignore_patterns = []
    with open(gitignore_path, "r") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("!"):
                continue

            pattern = line.replace("/", "").replace("*", "").split()[0].strip()
            ignore_patterns.append(pattern)

    return ignore_patterns


def detect_file_encoding(filename):
    """
    Detects the encoding of a file.

    Args:
    - filename (str): Path to the file to detect the encoding.

    Returns:
    - str: Encoding name detected.
    """
    with open(filename, 'rb') as rawdata:
        result = chardet.detect(rawdata.read())
    return result['encoding']


def save_data_to_json(filename, data):
    """
    Saves data to a JSON file.

    Args:
    - filename (str): Path to the JSON file to save.
    - data (dict): Data to be saved to the JSON file.
    """
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    # Example usage: finding Python files in a specific directory
    directory_path = r"c:\Users\aluno\AppData\Local\Programs\Python\Python310\Lib\site-packages\PIL"
    extension = ".py"

    python_files = find_files_with_extension(directory_path, extension)
    for file in python_files:
        print(file)
