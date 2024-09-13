import uuid
from .base import UMLRelationship, XmlElementFromString


class InheritanceRelationship(XmlElementFromString, UMLRelationship):
    """
    Represents an inheritance relationship in a UML diagram.

    Inherits from:
    - XmlElementFromString: Provides functionality to initialize from an XML string.
    - UMLRelationship: Defines common behavior for UML relationships.

    Attributes:
    - parent (str): The ID of the parent element in the UML diagram.
    - source (str): The ID of the source element (the class that is inheriting).
    - target (str): The ID of the target element (the class being inherited from).
    """

    def __init__(self, parent: str, source: str, target: str):
        """
        Initializes an InheritanceRelationship instance with a unique ID and XML representation.

        Args:
        - parent (str): The ID of the parent element.
        - source (str): The ID of the source element (the class that inherits).
        - target (str): The ID of the target element (the class being inherited from).
        """
        # Generate a unique ID for the inheritance relationship
        unique_id = f"inheritance-{uuid.uuid4()}"

        # Define the XML string representing the relationship
        xml_string = f"""
<mxCell id="{unique_id}"
        style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=block;endFill=0;"
        parent="{parent}" source="{source}" target="{target}" edge="1">
    <mxGeometry relative="1" as="geometry" />
</mxCell>
        """
        # Initialize the base class with the XML string
        super().__init__(xml_string)

class AssociationRelationship(XmlElementFromString, UMLRelationship):
    """
    Represents an Association relationship in a UML diagram.

    Inherits from:
    - XmlElementFromString: Provides functionality to initialize from an XML string.
    - UMLRelationship: Defines common behavior for UML relationships.

    Attributes:
    - parent (str): The ID of the parent element in the UML diagram.
    - source (str): The ID of the source element (the class that is inheriting).
    - target (str): The ID of the target element (the class being inherited from).
    """

    def __init__(self, parent: str, source: str, target: str):
        """
        Initializes an AssociationRelationship instance with a unique ID and XML representation.

        Args:
        - parent (str): The ID of the parent element.
        - source (str): The ID of the source element (the class that inherits).
        - target (str): The ID of the target element (the class being inherited from).
        """
        # Generate a unique ID for the association relationship
        unique_id = f"association-{uuid.uuid4()}"

        # Define the XML string representing the relationship
        xml_string = f"""
<mxCell id="{unique_id}"
        style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=none;endFill=0;strokeColor=#ff0000;"
        parent="{parent}" source="{source}" target="{target}" edge="1">
    <mxGeometry relative="1" as="geometry" />
</mxCell>
        """
        # Initialize the base class with the XML string
        super().__init__(xml_string)
