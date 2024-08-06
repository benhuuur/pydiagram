from pydiagram.uml_generator.managers import ElementConfigManager
import xml.etree.ElementTree as ET
from typing import List, Dict

from pydiagram.uml_generator.elements import mxCell, root, mxfile, diagram, mxGraphModel, classStroke, classField, classHeader
from pydiagram.uml_generator.utils import encapsulation_to_signal


class UMLClassBuilder:
    def __init__(self, configs: dict):
        self.x = None
        self.y = None
        self._configs = configs

    def create_class_elements(self, class_metadata: Dict, class_id: str, parent: ET.Element, details) -> \
            List[ET.Element]:
        """Creates UML class representation elements."""
        if not class_metadata or 'class_name' not in class_metadata:
            raise ValueError("Invalid class data provided.")

        elements: list[ET.Element] = []
        self.x, self.y = details["position"]

        parent_id = parent.attrib.get("id")

        header_style = self._configs["elements"]["classHeader"]["style"]
        header_dimensions = (
            self.x,
            self.y,
            self._configs["elements"]["classHeader"]["width"],
            None
        )

        header = classHeader(attrib={
            "id": f"class-{class_id}",
            "value": str(class_metadata["class_name"]),
            "style": header_style,
            "parent": str(parent_id)
        }, dimensions=header_dimensions)
        elements.append(header)

        header_id = header.attrib.get('id')

        self.y += 26
        attributes = self.create_class_attributes(
            class_metadata.get('attributes', []), header_id)
        elements.extend(attributes)

        self.y += 8
        stroke_dimensions = (
            self.y,
            self._configs["elements"]["classStroke"]["width"],
            self._configs["elements"]["classStroke"]["height"]
        )
        stroke = classStroke(dimensions=stroke_dimensions, attrib={
            'parent': str(header_id),
        })

        elements.append(stroke)

        self.y += 8
        methods = self.create_class_methods(
            class_metadata.get('methods', []), header_id)
        elements.extend(methods)

        header.find("mxGeometry").attrib["height"] = str(self.y)

        return elements

    def create_class_attributes(self, attributes_data: List[Dict], parent_id: str) -> List[ET.Element]:
        """Creates attributes for the UML class."""
        attributes = []
        style = self._configs["elements"]["classField"]["style"]
        height = self._configs["elements"]["classField"]["height"]
        width = self._configs["elements"]["classField"]["width"]

        for index, attribute in enumerate(attributes_data):
            dimensions = (self.y, width, height)
            attributes.append(
                classField(dimensions, attrib={
                    'id': f"attribute-{index}-{parent_id}",
                    'value': f"{encapsulation_to_signal(attribute['encapsulation'])} {attribute['name']}: {attribute['data_type']}",
                    'style': style,
                    'parent': str(parent_id),
                }))
            self.y += 26

        return attributes

    def create_class_methods(self, methods_data: List[Dict], parent_id: str) -> List[ET.Element]:
        """Creates methods for the UML class."""
        methods = []
        style = self._configs["elements"]["classField"]["style"]
        height = self._configs["elements"]["classField"]["height"]
        width = self._configs["elements"]["classField"]["width"]

        for index, method in enumerate(methods_data):
            dimensions = (self.y, width, height)
            current_method = classField(
                dimensions,
                attrib={
                    'id': f"method-{index}-{parent_id}",
                    'value': str(method["name"]),
                    'style': style,
                    'parent': str(parent_id),
                    'vertex': "1"
                })
            methods.append(current_method)
            self.y += 26

        return methods


class DrawioDiagramBuilder:
    def __init__(self) -> None:
        self.mxCell_count = 0
        self._root_element = root()
        self._root_element.append(mxCell(attrib={"id": "0"}))
        self._root_element.append(mxCell(attrib={"id": "1", "parent": "0"}))
        self.uml_class_count = 0
        self.configs = ElementConfigManager.get_manager().get_config()

    def append_class(self, details):
        """Adds a UML class to the diagram."""
        self.uml_class_count += 1
        builder = UMLClassBuilder(self.configs)
        parent = self._root_element.findall('*')[1]
        class_element = builder.create_class_elements(
            details["class"], str(self.uml_class_count), parent, details)

        self._root_element.extend(class_element)

    def build(self) -> ET.ElementTree:
        mxGraphModel_attributes = self.configs["elements"]["mxGraphModel"]["attributes"]
        var_mxGraphModel = mxGraphModel(mxGraphModel_attributes)
        var_mxGraphModel.append(self._root_element)

        diagram_attributes = self.configs["elements"]["diagram"]["attributes"]
        var_diagram = diagram(diagram_attributes)
        var_diagram.append(var_mxGraphModel)

        mxfile_attributes = self.configs["elements"]["mxfile"]["attributes"]
        var_mxfile = mxfile(mxfile_attributes)
        var_mxfile.append(var_diagram)

        return ET.ElementTree(var_mxfile)
