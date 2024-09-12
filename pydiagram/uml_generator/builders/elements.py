import xml.etree.ElementTree as ET
from typing import Dict, Any
from pydiagram.uml_generator.utils import Dimensions, encapsulation_signal
from pydiagram.uml_generator.elements import ClassAttribute, ClassStroke, ClassMethod


class AttributeBuilder:
    """
    A builder class for creating UML class attribute elements.

    Attributes:
        class_id (str): The ID of the UML class to which the attributes belong.
    """

    def __init__(self, class_id: str) -> None:
        """
        Initializes the AttributeBuilder with the class ID.

        Args:
            class_id (str): The ID of the UML class.
        """
        self.class_id = class_id

    def build(self, metadata: Dict[str, Any], dimensions: Dimensions) -> ET.Element:
        """
        Builds a UML class attribute element.

        Args:
            metadata (Dict[str, Any]): Metadata containing the name, encapsulation, and optional data type of the attribute.
            dimensions (Dimensions): The dimensions of the attribute element.

        Returns:
            ET.Element: An XML element representing the UML class attribute.

        Raises:
            KeyError: If required keys are missing in the metadata.
        """
        try:
            name = metadata["name"]
            encapsulation = encapsulation_signal(metadata["encapsulation"])
            data_type = metadata.get("data_type", "")
            return ClassAttribute(
                self.class_id, encapsulation, name, data_type, dimensions
            )
        except KeyError as e:
            raise KeyError(f"Missing required metadata key: {e}")


class StrokeBuilder:
    """
    A builder class for creating UML class stroke (separator) elements.

    Attributes:
        class_id (str): The ID of the UML class to which the stroke belongs.
    """

    def __init__(self, class_id: str) -> None:
        """
        Initializes the StrokeBuilder with the class ID.

        Args:
            class_id (str): The ID of the UML class.
        """
        self.class_id = class_id

    def build(self, dimensions: Dimensions) -> ET.Element:
        """
        Builds a UML class stroke element.

        Args:
            dimensions (Dimensions): The dimensions of the stroke element.

        Returns:
            ET.Element: An XML element representing the UML class stroke.
        """
        return ClassStroke(self.class_id, dimensions)


class MethodBuilder:
    """
    A builder class for creating UML class method elements.

    Attributes:
        class_id (str): The ID of the UML class to which the methods belong.
    """

    def __init__(self, class_id: str) -> None:
        """
        Initializes the MethodBuilder with the class ID.

        Args:
            class_id (str): The ID of the UML class.
        """
        self.class_id = class_id

    def build(self, metadata: Dict[str, Any], dimensions: Dimensions) -> ET.Element:
        """
        Builds a UML class method element.

        Args:
            metadata (Dict[str, Any]): Metadata containing the name, encapsulation, and arguments of the method.
            dimensions (Dimensions): The dimensions of the method element.

        Returns:
            ET.Element: An XML element representing the UML class method.

        Raises:
            KeyError: If required keys are missing in the metadata.
        """
        try:
            name = metadata["name"]
            encapsulation = encapsulation_signal(metadata["encapsulation"])
            args = ", ".join(metadata["args"])
            return ClassMethod(dimensions, encapsulation, name, args, self.class_id)
        except KeyError as e:
            raise KeyError(f"Missing required metadata key: {e}")
