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
        
        # Initialize the parent class with the root's tag and attributes
        super().__init__(root.tag, root.attrib)
        
        # Copy the text and tail from the root element
        self.text = root.text
        self.tail = root.tail
        
        # Extend the current element with the children from the root element
        super().extend(list(root))


class UMLRelationship(ABC):
    """
    Abstract base class for UML relationships.

    This class serves as a blueprint for UML relationship classes that require a parent,
    source, and target element ID.
    """

    @abstractmethod
    def __init__(self, parent: str, source: str, target: str) -> None:
        """
        Initializes the UMLRelationship with parent, source, and target IDs.

        Args:
            parent (str): The ID of the parent element.
            source (str): The ID of the source element.
            target (str): The ID of the target element.
        """
        pass
