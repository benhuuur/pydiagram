import json
import xml.etree.ElementTree as ET
from collections import namedtuple
from typing import Any, List, Optional, Dict


class Dimensions(namedtuple('Dimensions', ['x', 'y', 'width', 'height'])):
    """
    A class representing the dimensions of a rectangular area.

    Attributes:
    - x (int): The x-coordinate of the top-left corner.
    - y (int): The y-coordinate of the top-left corner.
    - width (int): The width of the rectangle.
    - height (int): The height of the rectangle.
    """
    __slots__ = ()


def create_element(parent: ET.Element, tag: str, attrib: Optional[Dict[str, str]] = None, text: Optional[str] = None) -> ET.Element:
    """
    Creates a new XML element as a child of the given parent element.

    Args:
    - parent (ET.Element): The parent element to which the new element will be added.
    - tag (str): The tag name of the new element.
    - attrib (Optional[Dict[str, str]]): A dictionary of attributes to set on the new element.
    - text (Optional[str]): Text content to set for the new element.

    Returns:
    - ET.Element: The newly created XML element.
    """
    element = ET.SubElement(parent, tag, attrib or {})
    if text:
        element.text = text
    return element


def contains_keys(d: Dict[str, Any], keys: List[str]) -> bool:
    """
    Checks if a dictionary contains all specified keys.

    Args:
    - d (Dict[str, Any]): The dictionary to check.
    - keys (List[str]): A list of keys to look for in the dictionary.

    Returns:
    - bool: True if all keys are present in the dictionary, False otherwise.
    """
    return all(key in d for key in keys)


def json_to_dict(json_path: str) -> Dict[str, Any]:
    """
    Reads a JSON file and converts it to a dictionary.

    Args:
    - json_path (str): The path to the JSON file to be read.

    Returns:
    - Dict[str, Any]: The dictionary representation of the JSON data.

    Raises:
    - IOError: If there is an error opening or reading the file.
    - json.JSONDecodeError: If there is an error decoding the JSON data.
    """
    try:
        with open(json_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error reading JSON file: {e}")
        raise


def save_xml(xml_content: ET.ElementTree, filename: str) -> None:
    """
    Saves an XML tree to a file.

    Args:
    - xml_content (ET.ElementTree): The XML tree to be saved.
    - filename (str): The path to the file where the XML tree will be saved.

    Raises:
    - IOError: If there is an error writing to the file.
    """
    try:
        xml_content.write(filename, encoding="utf-8", xml_declaration=True)
    except IOError as e:
        print(f"Error saving XML file: {e}")
        raise


def encapsulation_signal(encapsulation: str) -> str:
    """
    Converts encapsulation type to its corresponding UML signal.

    Args:
    - encapsulation (str): The encapsulation type ('Public' or 'Private').

    Returns:
    - str: The UML signal corresponding to the encapsulation type ('+' for Public, '-' for Private).

    Raises:
    - ValueError: If the encapsulation type is unknown.
    """
    if encapsulation == "Public":
        return "+"
    elif encapsulation == "Private":
        return "-"
    else:
        raise ValueError(f"Unknown encapsulation type: {encapsulation}")


def get_element_id(root: ET.Element, element_type: str, element_value: str) -> Optional[str]:
    """
    Finds the ID of an XML element based on its type and a specific attribute value.

    Args:
    - root (ET.Element): The root element of the XML tree.
    - element_type (str): The tag name of the element to search for.
    - element_value (str): The value of the 'value' attribute to match.

    Returns:
    - Optional[str]: The ID of the matching element, or None if no match is found.
    """
    for element in root.findall(element_type):
        if element.get('value') == element_value:
            return element.get('id')
    return None


def get_elements_by_attribute(root: ET.Element, attribute_name: str, attribute_value: str) -> List[ET.Element]:
    """
    Retrieves all XML elements that have a specific attribute with a given value.

    Args:
    - root (ET.Element): The root element of the XML tree.
    - attribute_name (str): The name of the attribute to check.
    - attribute_value (str): The value the attribute should have.

    Returns:
    - List[ET.Element]: A list of XML elements matching the specified attribute and value.
    """
    return [element for element in root.findall('.//*') if element.get(attribute_name) == attribute_value]
