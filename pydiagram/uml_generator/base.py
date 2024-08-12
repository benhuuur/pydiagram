from abc import ABC, abstractmethod
import xml.etree.ElementTree as ET


class XmlElementFromString(ET.Element):
    """
    An XML element created from an XML string.

    This class extends the functionality of the standard `xml.etree.ElementTree.Element` class
    to allow the initialization of an XML element directly from a string representation of XML data.

    Args:
        string (str): A string containing XML data. The string should be well-formed XML.
    """

    def __init__(self, string: str):
        try:
            root = ET.fromstring(string)
        except ET.ParseError as e:
            raise ValueError(f"The provided XML data is invalid: {e}")
        super().__init__(root.tag, root.attrib)
        self.text = root.text
        self.tail = root.tail
        self.extend(root)


class UMLRelationship(ABC):
    @abstractmethod
    def __init__(self, parent: str, source: str, target: str) -> None:
        """
        Initializes the UMLRelationship with parent, source, and target.

        :param parent: ID of the parent element.
        :param source: ID of the source element.
        :param target: ID of the target element.
        """
        pass