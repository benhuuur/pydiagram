import xml.etree.ElementTree as ET
from pydiagram.uml_generator.managers import ElementConfigManager
import pydiagram.uml_generator.utils as utils


class mxfile(ET.Element):
    _attributes = ["host", "agent"]

    def __init__(self, attrib: dict = ...):
        if utils.validate_dict(dict=attrib, keys=self._attributes):
            super().__init__("mxfile", attrib=attrib)
        else:
            raise Exception("Invalid Attibutes")


class diagram(ET.Element):
    _attributes = ["id", "name"]

    def __init__(self, attrib: dict = ...):
        if utils.validate_dict(dict=attrib, keys=self._attributes):
            super().__init__("diagram", attrib=attrib)
        else:
            raise Exception("Invalid Attibutes")


class mxGraphModel(ET.Element):
    _attributes = ['dx', 'dy', 'grid', 'gridSize', 'guides', 'tooltips', 'connect',
                   'arrows', 'fold', 'page', 'pageScale', 'pageWidth', 'pageHeight', 'math', 'shadow']

    def __init__(self, attrib: dict = ...):
        if utils.validate_dict(dict=attrib, keys=self._attributes):
            super().__init__("mxGraphModel", attrib=attrib)
        else:
            raise Exception("Invalid Attibutes")


class root(ET.Element):
    def __init__(self):
        super().__init__("root")


class mxCell(ET.Element):
    _attributes = ["id"]

    def __init__(self, attrib: dict = ...):
        if utils.validate_dict(attrib, self._attributes):
            super().__init__("mxCell", attrib=attrib)
        else:
            raise Exception("Invalid Attibutes")


class mxGeometry(ET.Element):
    _attributes = ["y", "width", "height", "as"]

    def __init__(self, attrib: dict = ...):
        if utils.validate_dict(attrib, self._attributes):
            super().__init__("mxGeometry", attrib=attrib)
        else:
            raise Exception("Invalid Attibutes")


class classHeader(mxCell):
    _attributes = ["id", "value", "style", "parent"]

    def __init__(self, dimensions: tuple[int, int, int, int], attrib: dict = ...):
        if utils.validate_dict(attrib, self._attributes):
            attrib['vertex'] = "1"
            super().__init__(attrib)
            x, y, width, height = dimensions
            self.append(mxGeometry(
                {'x': str(x), 'y': str(y), 'width': str(width), 'height': str(height), 'as': 'geometry'}))
        else:
            raise Exception("Invalid Attibutes")


class classField(mxCell):
    _attributes = ["id", "value", "style", "parent"]

    def __init__(self, dimensions: tuple[int, int, int, int], attrib: dict = ...):
        if utils.validate_dict(attrib, self._attributes):
            attrib['vertex'] = "1"

            super().__init__(attrib)
            y, width, height = dimensions
            self.append(mxGeometry(
                {'y': str(y), 'width': str(width), 'height': str(height), 'as': 'geometry'}))
        else:
            raise Exception("Invalid Attibutes")


class classStroke(mxCell):
    _attributes = ["parent"]

    def __init__(self, dimensions: tuple[int, int, int], attrib: dict = ...):
        configs = ElementConfigManager.get_manager().get_config()[
            "elements"]["classStroke"]
        styles = configs["style"]
        if utils.validate_dict(attrib, self._attributes):
            attrib['id'] = f"{attrib['parent']}-separator"

            attrib['style'] = styles
            attrib['value'] = ""
            attrib['vertex'] = "1"

            super().__init__(attrib)

            y, width, height = dimensions
            self.append(mxGeometry(
                {'y': str(y), 'width': str(width), 'height': str(height), 'as': 'geometry'}))
        else:
            raise Exception("Invalid Attibutes")
