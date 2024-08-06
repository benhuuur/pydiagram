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


def get_element_id(root: ET.Element, element_type: str, element_value: str) -> Optional[str]:
    """
    Retorna o ID de um elemento XML que corresponde ao tipo e valor fornecidos.

    Args:
        root (ET.Element): O elemento raiz do XML.
        element_type (str): O tipo do elemento a ser buscado (tag).
        element_value (str): O valor do atributo 'value' do elemento.

    Returns:
        Optional[str]: O ID do elemento correspondente ou None se não encontrado.
    """
    for element in root.findall(element_type):
        if element.get('value') == element_value:
            return element.get('id')
    return None


def get_elements_by_attribute(root: ET.Element, element_attribute: str, element_value: str) -> List[ET.Element]:
    """
    Retorna uma lista de elementos XML que possuem um atributo específico com um determinado valor.

    Args:
        root (ET.Element): O elemento raiz do XML.
        element_attribute (str): O nome do atributo a ser verificado.
        element_value (str): O valor que o atributo deve ter.

    Returns:
        List[ET.Element]: Uma lista de elementos que correspondem ao atributo e valor fornecidos.
    """
    elements = []
    for element in root.findall('.//*'):  # Busca todos os elementos
        if element.get(element_attribute) == element_value:
            elements.append(element)
    return elements
