import uuid
from .base import UMLRelationship, XmlElementFromString


class InheritanceRelationship(XmlElementFromString, UMLRelationship):
    def __init__(self, parent: str, source: str, target: str):
        unique_id = f"inheritance-{uuid.uuid4()}"

        xml_string = f"""
<mxCell id="{unique_id}"
        style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=block;endFill=0;"
        parent="{parent}" source="{source}" target="{target}" edge="1">
    <mxGeometry relative="1" as="geometry" />
</mxCell>
        """
        super().__init__(xml_string)