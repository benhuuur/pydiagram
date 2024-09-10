import xml.etree.ElementTree as ET

from typing import Any, Dict
from pydiagram.uml_generator.utils import Dimensions, encapsulation_signal


class AttributeBuilder:
    def __init__(self, class_id: str):
        self.class_id = class_id

    def build(self, metadata: Dict[str, Any], dimensions: Dimensions) -> ET.Element:
        from pydiagram.uml_generator.elements import ClassAttribute
        name = metadata["name"]
        encapsulation = encapsulation_signal(metadata["encapsulation"])
        data_type = metadata.get("data_type", "")
        attribute = ClassAttribute(
            self.class_id, encapsulation, name, data_type, dimensions)
        return attribute


class StrokeBuilder:
    def __init__(self, class_id: str):
        self.class_id = class_id

    def build(self, dimensions: Dimensions) -> ET.Element:
        from pydiagram.uml_generator.elements import ClassStroke
        return ClassStroke(self.class_id, dimensions)


class MethodBuilder:
    def __init__(self, class_id: str):
        self.class_id = class_id

    def build(self, metadata: Dict[str, Any], dimensions: Dimensions) -> ET.Element:
        from pydiagram.uml_generator.elements import ClassMethod
        name = metadata["name"]
        encapsulation = encapsulation_signal(metadata["encapsulation"])
        args = ", ".join(metadata["args"])
        return ClassMethod(dimensions, encapsulation, name, args, self.class_id)
