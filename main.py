from abc import ABC
from collections import namedtuple
import json
import xml.etree.ElementTree as ET
import uuid

from pydiagram.py_class_extractor import generate_classes_dicts_from_file

# from pydiagram.uml_generator import utils

if __name__ == "__main__":
    def encapsulation_signal(encapsulation: str):
        if encapsulation == "Public":
            return "+"
        return "-"

    class Inheritance(ET.Element):
        def __init__(self, parent, source, target):
            root = ET.fromstring(f"""
        <mxCell id="M5yhiGJmRxRB3JF-EFZL-{uuid.uuid4()}"
                    style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=block;endFill=0;"
                    parent="{parent}" source="{source}"
                    target="{target}" edge="1">
                <mxGeometry relative="1" as="geometry" />
        </mxCell>
            """)
            super().__init__(root.tag, root.attrib)
            self.text = root.text
            self.tail = root.tail
            self.extend(root)

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
            real_root = self.find('diagram/mxGraphModel/root')
            if real_root:
                return real_root.append(subelement)
            super().append(subelement)

        def extend(self, elements) -> None:
            real_root = self.find('diagram/mxGraphModel/root')
            if real_root is not None:
                return real_root.extend(elements)
            super().extend(elements)

    class Dimensions(namedtuple('Dimensions', ['x', 'y', 'width', 'height'])):
        # block dicts from this class
        __slots__ = ()

        # return tuple
        def __new__(cls, x, y, width, height):
            return super(Dimensions, cls).__new__(cls, x, y, width, height)

    class Class(ET.Element):
        def __init__(self, metadata: dict, dimensions: Dimensions, parent: any):
            self.id = f"class-{uuid.uuid4()}"

            y = dimensions.y + 26
            for attribute in metadata["attributes"]:
                attribute_dimensions = Dimensions(
                    0, y, dimensions.width, dimensions.height, )
                self._append_attribute(attribute, attribute_dimensions)
                y += 26

            stroke_height = 8
            stroke_dimensions = Dimensions(
                dimensions.x, y, dimensions.width, stroke_height)
            self._append_stroke(stroke_dimensions)
            y += stroke_height

            for attribute in metadata["methods"]:
                attribute_dimensions = Dimensions(
                    0, y, dimensions.width, dimensions.height)
                self._append_method(attribute, attribute_dimensions)
                y += 26

            final_dimensions = Dimensions(
                dimensions.x, dimensions.y, dimensions.width, y)
            self._append_header(metadata, final_dimensions, parent)

        def _append_attribute(self, metadata: dict, dimensions: Dimensions):
            name = metadata["name"]
            # encapsulation = utils.encapsulation_signal(
            #     metadata["encapsulation"])
            encapsulation = metadata["encapsulation"]
            encapsulation = encapsulation_signal(encapsulation)
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

        def _append_stroke(self, dimensions: Dimensions):
            x, y, width, height = dimensions
            stroke = ET.fromstring(f"""
<mxCell id="stroke-{uuid.uuid4()}-{self.id}" value=""
    style="line;strokeWidth=1;fillColor=none;align=left;verticalAlign=middle;spacingTop=-1;spacingLeft=3;spacingRight=3;rotatable=0;labelPosition=right;points=[];portConstraint=eastwest;strokeColor=inherit;"
    parent="{self.id}" vertex="1">
        <mxGeometry y="{y}" width="{width}" height="{height}" as="geometry" />
</mxCell>
        """)
            self.append(stroke)

        def _append_method(self, metadata: dict, dimensions: Dimensions):
            name = metadata["name"]
            # encapsulation = utils.encapsulation_signal(
            #     metadata["encapsulation"])
            encapsulation = metadata["encapsulation"]
            encapsulation = encapsulation_signal(encapsulation)
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
            name = metadata["name"]

            x, y, width, height = dimensions

            header = ET.fromstring(f"""
<mxCell id="{self.id}" value="{name}"
    style="swimlane;fontStyle=1;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=26;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;whiteSpace=wrap;html=1;"
    parent="{parent}" vertex="1">
    <mxGeometry x="{x}" y="{y}" width="{width}" height="{height}" as="geometry">
    </mxGeometry>
</mxCell>
            """)

            return self.insert(0, header)

    diagram = Diagram("pydiagram")
    metadata = generate_classes_dicts_from_file(r"C:\Users\Aluno\Desktop\pydiagram\teste.py")
    # with open('class.json', "r") as file:
    #     metadata = json.load(file)
    x = 0
    classes = list()
    for class_metadata in metadata:
        dimensions = Dimensions(x, 0, 160, 26)
        UML_class = Class(class_metadata, dimensions, diagram.class_parent)
        classes.append(UML_class)
        x += 170

    relationships = list()
    for source_index, source_class_metadata in enumerate(metadata):
        for relationship in source_class_metadata["relationships"]:
            if relationship["type"] == "inheritance":
                for target_index, target_class_metadata in enumerate(metadata):
                    if relationship["related"] == target_class_metadata["name"]:
                        relationships.append(Inheritance(
                            diagram.class_parent, classes[source_index].id, classes[target_index].id))
                        break

    diagram.extend(relationships)
    diagram.extend(classes)
    with open('output.xml', 'w', encoding='utf-8') as file:
        file.write(ET.tostring(diagram, encoding='unicode'))
