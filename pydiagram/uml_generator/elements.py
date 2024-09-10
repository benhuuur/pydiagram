import uuid
import xml.etree.ElementTree as ET

from .base import XmlElementFromString
import pydiagram.uml_generator.utils as utils


class DrawIODiagram(XmlElementFromString):
    """
    Represents a Draw.io (diagrams.net) diagram in XML format.

    Attributes:
        id (uuid.UUID): A unique identifier for the diagram.
        default_parent_id (int): The ID of the default parent cell, used as a reference for child elements.
    """

    def __init__(self, name):
        """
        Args:
            name (str): The name of the diagram.
        """
        self.id = uuid.uuid4()
        self.default_parent_id = 1
        string = f"""
<mxfile host="app.diagrams.net" agent="Python Script">
<diagram id="{self.id}" name="{name}">
   <mxGraphModel dx="1434" dy="780" grid="1" gridSize="10" guides="1" tooltips="1" connect="1"
arrows="1" fold="1" page="1" pageScale="1" pageWidth="827" pageHeight="1169" math="0"
shadow="0">
        <root>
            <mxCell id="0" />
            <mxCell id="{self.default_parent_id}" parent="0" />
        </root>
    </mxGraphModel>
</diagram>
</mxfile>
"""
        super().__init__(string)

    def append(self, subelement: ET.Element) -> None:
        diagram_root = self.find('diagram/mxGraphModel/root')
        if diagram_root:
            return diagram_root.append(subelement)
        super().append(subelement)

    def extend(self, elements) -> None:
        diagram_root = self.find('diagram/mxGraphModel/root')
        if diagram_root is not None:
            return diagram_root.extend(elements)
        super().extend(elements)


class UMLClassDiagramElement(ET.Element):
    """
    Represents an element in a UML class diagram.

    This class creates a UML class element with its attributes, methods, and header,
    and appends them to the XML structure. It uses builders to create and configure
    the various components of the UML class diagram.

    Attributes:
        id (str): A unique identifier for the UML class element.
        _metadata (dict): Metadata containing information about attributes and methods.
        _dimensions (utils.Dimensions): Dimensions of the UML class element.
        _parent (Any): Parent element to which this UML class element will be attached.

    Methods:
        _build_class() -> None:
            Constructs and appends the various components of the UML class element.
    """

    def __init__(self, metadata: dict, dimensions: utils.Dimensions, parent: any):
        """
        Args:
            metadata (dict): Metadata dictionary containing details of attributes and methods.
            dimensions (utils.Dimensions): Dimensions of the UML class element including position and size.
                Note: The `height` value in `dimensions` is provided for completeness but will be updated 
                based on the final layout. The caller does not need to provide the exact final height.
            parent (Any): The parent element to which this UML class element will be appended.
        """
        self.id = f"class-{uuid.uuid4()}"
        self._metadata = metadata
        self._dimensions = dimensions
        self._parent = parent
        self._build_class()

    def _build_class(self):
        """
        Builds the UML class element by adding attributes, a stroke, methods, and a header.

        The method:
        1. Adds attributes with a specified y-offset increment.
        2. Adds a stroke to separate the attributes from methods.
        3. Adds methods with a specified y-offset increment.
        4. Adds a header at the top of the UML class element.

        The y-offsets are adjusted as elements are added, and the final dimensions are updated.
        """
        from .builders.elements import AttributeBuilder, MethodBuilder, StrokeBuilder

        incremented_y_axios = 26
        # incremented_y_axios = self._dimensions.y + 26

        # Create and append attributes
        attribute_builder = AttributeBuilder(self.id)
        for attribute in self._metadata["attributes"]:
            attribute_dimensions = utils.Dimensions(
                0, incremented_y_axios, self._dimensions.width, 26)
            attribute_element = attribute_builder.build(
                attribute, attribute_dimensions)
            self.append(attribute_element)
            incremented_y_axios += 26

         # Create and append stroke
        stroke_builder = StrokeBuilder(self.id)
        stroke_dimensions = utils.Dimensions(
            self._dimensions.x, incremented_y_axios, self._dimensions.width, 8)
        stroke_element = stroke_builder.build(stroke_dimensions)
        self.append(stroke_element)
        incremented_y_axios += 8

        # Create and append methods
        method_builder = MethodBuilder(self.id)
        for method in self._metadata["methods"]:
            method_dimensions = utils.Dimensions(
                0, incremented_y_axios, self._dimensions.width, 26)
            method_element = method_builder.build(method, method_dimensions)
            self.append(method_element)
            incremented_y_axios += 26

        # Create and append header
        header_dimensions = utils.Dimensions(
            self._dimensions.x, self._dimensions.y, self._dimensions.width, incremented_y_axios)
        header_element = ClassHeader(
            self._metadata["name"], header_dimensions, self._parent, self.id)
        self.insert(0, header_element)

        self._dimensions = utils.Dimensions(
            self._dimensions.x, self._dimensions.y, self._dimensions.width, height=incremented_y_axios)


class ClassHeader(XmlElementFromString):
    """
    Represents the header of a UML class diagram element.

    This class generates an XML representation for the header section of a UML class diagram.
    The header typically includes the class name and its configuration as specified by the `mxCell` tag.
    """

    def __init__(self, name: str, dimensions: tuple, parent: str, id: str):
        """
        Args:
            name (str): The name to be displayed in the header.
            dimensions (tuple): A tuple containing (x, y, width, height).
            parent (str): The ID of the parent element.
            id (str): Unique identifier for this header element.
        """
        x, y, width, height = dimensions
        xml_string = f"""
<mxCell id="{id}" value="{name}"
style="swimlane;fontStyle=1;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=26;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;whiteSpace=wrap;html=1;"
parent="{parent}" vertex="1">
    <mxGeometry x="{x}" y="{y}" width="{width}" height="{height}" as="geometry">
    <mxRectangle x="{x}" y="{y}" width="{width-20}" height="30" as="alternateBounds" />
    </mxGeometry>
</mxCell>
        """
        super().__init__(xml_string)


class ClassMethod(XmlElementFromString):
    """
    Represents a method in a UML class diagram.

    This class generates an XML representation for a method element within a UML class diagram.
    The method is displayed with its encapsulation, name, and arguments.
    """

    def __init__(self, dimensions: tuple, encapsulation: str, name: str, args: str, parent: str):
        """
        Args:
            dimensions (tuple): A tuple containing (x, y, width, height) where:
                - x (int): Not used.
                - y (int): The y-coordinate of the method element.
                - width (int): The width of the method element.
                - height (int): The height of the method element.
            encapsulation (str): The encapsulation level of the method (e.g., public, private).
            name (str): The name of the method.
            args (str): The method arguments in string format.
            parent (str): The ID of the parent element in the XML structure.
        """
        x, y, width, height = dimensions
        xml_string = f"""
<mxCell id="method-{uuid.uuid4()}-{parent}" value="{encapsulation} {name}({args})"
style="text;align=left;verticalAlign=top;spacingLeft=4;spacingRight=4;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;"
parent="{parent}" vertex="1">
    <mxGeometry y="{y}" width="{width}" height="{height}" as="geometry" />
</mxCell>
        """
        super().__init__(xml_string)


class ClassStroke(XmlElementFromString):
    """
    Represents a stroke (or separator) in a UML class diagram.

    This class generates an XML representation for a stroke element, which is used
    to separate different sections of a UML class, such as attributes and methods.
    """

    def __init__(self, parent: str, dimensions: tuple):
        """
        Args:
            parent (str): The ID of the parent element in the XML structure.
            dimensions (tuple): A tuple containing (x, y, width, height) where:
                - x (int): Not used.
                - y (int): The y-coordinate of the stroke element.
                - width (int): The width of the stroke element.
                - height (int): The height of the stroke element.
        """
        x, y, width, height = dimensions
        xml_string = f"""
<mxCell id="stroke-{uuid.uuid4()}-{parent}" value=""
style="line;strokeWidth=1;fillColor=none;align=left;verticalAlign=middle;spacingTop=-1;spacingLeft=3;spacingRight=3;rotatable=0;labelPosition=right;points=[];portConstraint=eastwest;strokeColor=inherit;"
parent="{parent}" vertex="1">
    <mxGeometry y="{y}" width="{width}" height="{height}" as="geometry" />
</mxCell>
        """
        super().__init__(xml_string)


class ClassAttribute(XmlElementFromString):
    """
    Represents an attribute in a UML class diagram.

    This class generates an XML representation for an attribute element, which is
    used to display attributes of a UML class, including its encapsulation, name,
    and data type.
    """

    def __init__(self, parent: str, encapsulation: str, name: str, data_type: str, dimensions: tuple):
        """
        Args:
            parent (str): The ID of the parent element in the XML structure.
            encapsulation (str): The encapsulation level of the attribute (e.g., public, private).
            name (str): The name of the attribute.
            data_type (str): The data type of the attribute.
            dimensions (tuple): A tuple containing (x, y, width, height) where:
                - x (int): Not used.
                - y (int): The y-coordinate of the attribute element.
                - width (int): The width of the attribute element.
                - height (int): The height of the attribute element.
        """
        x, y, width, height = dimensions
        xml_string = f"""
<mxCell id="attribute-{uuid.uuid4()}-{parent}" value="{encapsulation} {name}: {data_type}"
        style="text;align=left;verticalAlign=top;spacingLeft=4;spacingRight=4;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;"
        parent="{parent}" vertex="1">
    <mxGeometry y="{y}" width="{width}" height="{height}" as="geometry" />
</mxCell>
        """
        super().__init__(xml_string)
