import json
import os
import chardet
from abc import ABC, abstractmethod
from typing import List, Optional


class SerializableToDict(ABC):
    """
    Abstract base class for objects that can be serialized to a dictionary.
    """

    @abstractmethod
    def to_dictionary(self) -> dict:
        """
        Converts the object to a dictionary representation.

        Returns:
            dict: Dictionary representation of the object.
        """
        pass


def get_files_recursively(directory: str, ignore_patterns: Optional[List[str]] = None) -> List[str]:
    """
    Recursively retrieves all files in a directory and its subdirectories.

    Args:
        directory (str): Directory path to start exploring.
        ignore_patterns (Optional[List[str]]): List of patterns for files to be ignored.

    Returns:
        List[str]: List of file paths found in the directory and its subdirectories.
    """
    if ignore_patterns is None:
        ignore_patterns = []

    files = []

    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)

        if any(pattern in item_path for pattern in ignore_patterns):
            continue

        if os.path.isdir(item_path):
            files.extend(get_files_recursively(item_path, ignore_patterns))
        elif os.path.isfile(item_path):
            files.append(item_path)

    return files


def find_files_with_extension(directory: str, extension: str) -> List[str]:
    """
    Recursively finds all files with a specific extension in a directory and its subdirectories.

    Args:
        directory (str): Directory path to start exploring.
        extension (str): Extension of the files to search for (e.g., '.py').

    Returns:
        List[str]: List of file paths that have the specified extension.
    """
    files = []

    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            files.extend(find_files_with_extension(item_path, extension))
        elif item.endswith(extension):
            files.append(item_path)

    return files


def read_gitignore_patterns(gitignore_path: str) -> List[str]:
    """
    Reads a .gitignore file and extracts patterns for ignored files.

    Args:
        gitignore_path (str): Path to the .gitignore file.

    Returns:
        List[str]: List of patterns for files to be ignored.
    """
    ignore_patterns = []
    with open(gitignore_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("!"):
                continue

            pattern = line.split()[0].strip()
            ignore_patterns.append(pattern)

    return ignore_patterns


def detect_file_encoding(filename: str) -> str:
    """
    Detects the encoding of a file.

    Args:
        filename (str): Path to the file to detect the encoding.

    Returns:
        str: Encoding name detected.
    """
    with open(filename, 'rb') as rawdata:
        result = chardet.detect(rawdata.read())
    return result['encoding']


def save_data_to_json(filename: str, data: dict):
    """
    Saves data to a JSON file.

    Args:
        filename (str): Path to the JSON file to save.
        data (dict): Data to be saved to the JSON file.
    """
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
