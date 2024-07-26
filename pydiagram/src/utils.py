import json
import xml.etree.ElementTree as ET


def create_element(parent, tag, attrib=None, text=None):
    element = ET.SubElement(parent, tag, attrib or {})
    if text:
        element.text = text
    return element


def validate_dict(dict, keys):
    return all(key in dict for key in keys)


def json_to_dict(json_path):
    with open(json_path, "r") as file:
        return json.load(file)


def save_xml(xml_content: ET.ElementTree, filename):
    xml_content.write(filename, encoding="utf-8")


def encapsulation_to_signal(encapsulation: str):
    if encapsulation == "Public":
        return "+"
    return "-"
