from abc import ABC
from collections import namedtuple
import json
import xml.etree.ElementTree as ET
import uuid

# from pydiagram.uml_generator import utils

if __name__ == "__main__":
    class Diagram(ET.Element):
        def __init__(self, name):
            self.id = uuid.uuid4()
            self.class_parent = 1
            root = ET.fromstring(
                f"""
<mxfile host="app.diagrams.net" agent="Python Script">
    <diagram id="{self.id}" name="{name}">
       <mxGraphModel dx="1434" dy="780" grid="1" gridSize="10" guides="1" tooltips="1" connect="1"
    arrows="1" fold="1" page="1" pageScale="1" pageWidth="827" pageHeight="1169" math="0"
    shadow="0">
            <root>
                <mxCell id="0" />
                <mxCell id="{self.class_parent}" parent="0" />
            </root>
        </mxGraphModel>
    </diagram>
</mxfile>
"""
            )
            super().__init__(root.tag, root.attrib)
            self.text = root.text
            self.tail = root.tail
            self.extend(root)

        def append(self, subelement: ET.Element) -> None:
            real_root = diagram.find('diagram/mxGraphModel/root')
            if isinstance(subelement, Container):
                real_root.extend(subelement.elements)
            real_root.append(subelement)

        #TODO        
        # def extend(self, elements: ET.Iterable[ET.Element]) -> None:
        #     real_root = diagram.find('diagram/mxGraphModel/root')
        #     if any(isinstance(item, Container) for item in array):
        #             real_root.extend(element.elements)
        #         real_root.append(element)

    class Container(ABC):
        def __init__(self):
            self.elements = list()

    class Dimensions(namedtuple('Dimensions', ['x', 'y', 'width', 'height'])):
        # block dicts from this class
        __slots__ = ()

        # return tuple
        def __new__(cls, x, y, width, height):
            return super(Dimensions, cls).__new__(cls, x, y, width, height)

    class Class(ET.Element, Container):
        def __init__(self, metadata: dict, dimensions: Dimensions, parent: any):
            Container.__init__(self)
            self.id = f"class-{uuid.uuid4()}"
            self._children = []

            for attribute in metadata["attributes"]:
                y = dimensions.y+26
                attribute_dimensions = Dimensions(
                   0, y, dimensions.width, dimensions.height, )
                self._append_attribute(attribute, attribute_dimensions)

            for attribute in metadata["methods"]:
                y = dimensions.y+26
                attribute_dimensions = Dimensions(
                    0, y, dimensions.width, dimensions.height)
                self._append_method(attribute, attribute_dimensions)

            self._append_header(metadata, dimensions, parent)

        def _append_attribute(self, metadata: dict, dimensions: Dimensions):
            name = metadata["name"]
            # encapsulation = utils.encapsulation_signal(
            #     metadata["encapsulation"])
            encapsulation = metadata["encapsulation"]
            data_type = metadata.get("data_type", "")

            x, y, width, height = dimensions

            attribute = ET.fromstring(f"""
<mxCell id="attribute-{uuid.uuid4()}-{self.id}" value="{encapsulation} {name}: {data_type}"
            style="text;align=left;verticalAlign=top;spacingLeft=4;spacingRight=4;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;"
            parent="{self.id}" vertex="1">
            <mxGeometry y="{y}" width="{width}" height="{height}" as="geometry" />
</mxCell>
            """)

            self.append(attribute)

        def _append_method(self, metadata: dict, dimensions: Dimensions):
            name = metadata["name"]
            encapsulation = "TODO"  # TODO
            args = ", ".join(metadata["args"])

            x, y, width, height = dimensions

            method = ET.fromstring(f"""
<mxCell id="method-{uuid.uuid4()}-{self.id}" value="{encapsulation} {name}({args})"
    style="text;align=left;verticalAlign=top;spacingLeft=4;spacingRight=4;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;"
    parent="{self.id}" vertex="1">
    <mxGeometry y="{y}" width="{width}" height="{height}" as="geometry" />
</mxCell>
            """)

            self.append(method)

        def _append_header(self, metadata: dict, dimensions: Dimensions, parent: any):
            name = metadata["class_name"]

            x, y, width, height = dimensions

            header = ET.fromstring(f"""
<mxCell id="{self.id}" value="{name}"
    style="swimlane;fontStyle=1;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=26;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;whiteSpace=wrap;html=1;"
    parent="{parent}" vertex="1">
    <mxGeometry x="{x}" y="{y}" width="{width}" height="{height}" as="geometry" />
</mxCell>
            """)
            return header

    diagram = Diagram("pydiagram")
    with open('class.json', "r") as file:
        metadata = json.load(file)
    x=0
    classes = list()
    for class_metadata in metadata:
        dimensions = Dimensions(x,0, 160, 26)
        classes.append(Class(metadata[0], dimensions, diagram.class_parent))
        x+=170
    
    diagram.extend(classes)
    
    with open('output.txt', 'w', encoding='utf-8') as file:
        file.write(ET.tostring(diagram, encoding='unicode'))
