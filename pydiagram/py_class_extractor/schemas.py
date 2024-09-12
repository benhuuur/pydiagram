from typing import Any, Tuple
from dataclasses import dataclass
from pydiagram.py_class_extractor.file_management import SerializableToDict


@dataclass
class AttributeInformation:
    """
    Data class to store information about an attribute.
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
    args: Tuple[str]  
    return_value: Any
    encapsulation: str


@dataclass
class RelationshipInformation:
    """
    Data class to store information about a UML relationship.
    """
    relation_type: str
    name  : str
    modules: Tuple[str]  


@dataclass
class ClassInformation(SerializableToDict):
    """
    Data class to store information about a class.

    Attributes:
    - modules (Tuple[str]): Tuple of module names where the class is defined.
    - name (str): The name of the class.
    - relationships (Tuple[RelationshipInformation]): Tuple of RelationshipInformation objects representing relationships with other classes.
    - attributes (Tuple[AttributeInformation]): Tuple of AttributeInformation objects representing attributes of the class.
    - methods (Tuple[FunctionInformation]): Tuple of FunctionInformation objects representing methods of the class.
    """
    modules: Tuple[str]  
    name: str
    relationships: Tuple[RelationshipInformation]  
    attributes: Tuple[AttributeInformation]  
    methods: Tuple[FunctionInformation]  

    def to_dictionary(self) -> dict:
        """
        Converts the ClassInformation object into a dictionary representation suitable for JSON serialization.

        Returns:
        - dict: A dictionary containing the class information.
            {
                "modules": Tuple[str],                      # Tuple of module names where the class is defined.
                "name": str,                               # The name of the class.
                "relationships": Tuple[dict],              # Tuple of dictionaries representing relationships (RelationshipInformation objects).
                "attributes": Tuple[dict],                 # Tuple of dictionaries representing attributes (AttributeInformation objects).
                "methods": Tuple[dict]                     # Tuple of dictionaries representing methods (FunctionInformation objects).
            }
        """
        return {
            "name": self.name,
            "modules": self.modules,
            "relationships": [relationship.__dict__ for relationship in self.relationships],
            "attributes": [attribute.__dict__ for attribute in self.attributes],
            "methods": [method.__dict__ for method in self.methods],
        }
