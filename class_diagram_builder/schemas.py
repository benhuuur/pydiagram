from typing import Any, List
from dataclasses import dataclass
from class_diagram_builder.file_management import SerializableToDict


@dataclass
class AttributeInformation:
    """
    Data class to store information about a attribute assignment.
    """

    name: str
    data_type: str
    encapsulation: str


@dataclass
class FunctionInformation:
    """
    Data class to store information about a function.
    """

    name: str
    args: List[str]
    return_value: Any


@dataclass
class ClassInformation(SerializableToDict):
    """
    Data class to store information about a class.

    Attributes:
    - name (str): The name of the class.
    - inheritance (List[str]): List of inherited class names.
    - attributes (List[AttributeInfo]): List of AttributeInfo objects representing attributes.
    - methods (List[FunctionInfo]): List of FunctionInfo objects representing methods.
    """

    name: str
    inheritance: List[str]
    attributes: List[AttributeInformation]
    methods: List[FunctionInformation]

    def to_dictionary(self) -> dict:
        """
        Converts the ClassInfo object into a dictionary representation suitable for JSON serialization.

        Returns:
        - dict: A dictionary containing the class information.
            {
                "class_name": str,          # The name of the class.
                "inheritance": List[str],   # List of inherited class names.
                "attributes": List[dict],   # List of dictionaries representing attributes (AttributeInfo objects).
                "methods": List[dict]       # List of dictionaries representing methods (FunctionInfo objects).
            }
        """
        return {
            "class_name": self.name,
            "inheritance": self.inheritance,
            "attributes": [attribute.__dict__ for attribute in self.attributes],
            "methods": [method.__dict__ for method in self.methods],
        }
