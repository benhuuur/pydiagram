from typing import List, Optional, Any, Tuple
from pathlib import Path


def extract_sublist_between(arr: List[Any], start: Any, end: Optional[Any] = None) -> List[Any]:
    """
    Extracts a contiguous sublist from a given list starting from the specified start value up to (and including) the end value.

    Args:
    - arr (List[Any]): The list from which to extract the sublist.
    - start (Any): The value to start the extraction from.
    - end (Optional[Any], optional): The value to end the extraction at. If not provided, the sublist will go from the start value to the end of the list.

    Returns:
    - List[Any]: A sublist starting from the start value up to (and including) the end value. If no end value is provided, the sublist extends to the end of the list.

    Raises:
    - ValueError: If start or end values are not found in the list, or if start appears after end.

    Example:
    >>> extract_sublist_between(["a", "b", "c", "d", "e"], "b", "d")
    ['b', 'c', 'd']

    >>> extract_sublist_between(["a", "b", "c", "d", "e"], "b")
    ['b', 'c', 'd', 'e']
    """
    if start not in arr:
        raise ValueError("Start value not found in the list")
    start_index = arr.index(start)
    if end is None:
        return arr[start_index:]

    if end not in arr:
        raise ValueError("End value not found in the list")
    end_index = arr.index(end)

    if start_index > end_index:
        raise ValueError(
            "Start value must appear before end value in the list")

    return arr[start_index:end_index + 1]


def split_path(module_path: str) -> Tuple[str, ...]:
    """
    Splits a file path into its component parts and removes the file extension.

    Args:
    - module_path (str): The path to the Python module file.

    Returns:
    - Tuple[str, ...]: A tuple containing the path components with the file extension removed.

    Example:
    >>> split_path("src/utils/helpers.py")
    ('src', 'utils', 'helpers')
    """
    path = Path(module_path)

    # Extract parts of the path and remove the '.py' extension from the last part
    path_parts = [part for part in path.with_suffix(
        '').parts if part]  # Avoid empty strings

    return tuple(path_parts)
