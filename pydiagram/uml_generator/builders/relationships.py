from pydiagram.uml_generator.base import UMLRelationship
from typing import Type


class RelationshipBuilder:
    """
    A builder class for creating UML relationships.

    This class facilitates the creation of UML relationship objects by providing
    a method to build a relationship between a source and a target with a specified parent.

    Attributes:
        parent (str): The ID of the parent element.
        source (str): The ID of the source element.
    """

    def __init__(self, parent: str, source: str) -> None:
        """
        Initializes the RelationshipBuilder with the parent and source IDs.

        Args:
            parent (str): The ID of the parent element.
            source (str): The ID of the source element.
        """
        self.parent = parent
        self.source = source

    def build(self, relationship_class: Type[UMLRelationship], target: str) -> UMLRelationship:
        """
        Builds a UML relationship object.

        Args:
            relationship_class (Type[UMLRelationship]): A subclass of UMLRelationship
                that represents the type of relationship to create.
            target (str): The ID of the target element.

        Returns:
            UMLRelationship: An instance of the specified UMLRelationship subclass.

        Raises:
            TypeError: If `relationship_class` is not a subclass of `UMLRelationship`.
        """
        if not issubclass(relationship_class, UMLRelationship):
            raise TypeError(f"{relationship_class} is not a subclass of UMLRelationship")
        
        return relationship_class(self.parent, self.source, target)
