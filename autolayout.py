import json
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import pydot_layout
import pydot

# Define the structure of the classes
class_data = [
    {"name": "XmlElementFromString", "modules": ["uml_generator", "base"], "relationships": [{"type": "inheritance", "related_module": ["xml", "etree", "ElementTree"], "related": "Element"}], "attributes": [{"name": "text", "data_type": None, "encapsulation": "Public"}, {"name": "tail", "data_type": None, "encapsulation": "Public"}], "methods": [{"name": "__init__", "args": ["self", "string"], "return_value": None, "encapsulation": "Public"}]},
    {"name": "UMLRelationship", "modules": ["uml_generator", "base"], "relationships": [{"type": "inheritance", "related_module": ["abc"], "related": "ABC"}], "attributes": [], "methods": [{"name": "__init__", "args": ["self", "parent", "source", "target"], "return_value": None, "encapsulation": "Public"}]},
    {"name": "AttributeBuilder", "modules": ["uml_generator", "builders", "elements"], "relationships": [], "attributes": [{"name": "class_id", "data_type": None, "encapsulation": "Public"}], "methods": [{"name": "__init__", "args": ["self", "class_id"], "return_value": None, "encapsulation": "Public"}, {"name": "build", "args": ["self", "metadata", "dimensions"], "return_value": None, "encapsulation": "Public"}]},
    {"name": "StrokeBuilder", "modules": ["uml_generator", "builders", "elements"], "relationships": [], "attributes": [{"name": "class_id", "data_type": None, "encapsulation": "Public"}], "methods": [{"name": "__init__", "args": ["self", "class_id"], "return_value": None, "encapsulation": "Public"}, {"name": "build", "args": ["self", "dimensions"], "return_value": None, "encapsulation": "Public"}]},
    {"name": "MethodBuilder", "modules": ["uml_generator", "builders", "elements"], "relationships": [], "attributes": [{"name": "class_id", "data_type": None, "encapsulation": "Public"}], "methods": [{"name": "__init__", "args": ["self", "class_id"], "return_value": None, "encapsulation": "Public"}, {"name": "build", "args": ["self", "metadata", "dimensions"], "return_value": None, "encapsulation": "Public"}]},
    {"name": "RelationshipBuilder", "modules": ["uml_generator", "builders", "relationships"], "relationships": [], "attributes": [{"name": "parent", "data_type": None, "encapsulation": "Public"}, {"name": "source", "data_type": None, "encapsulation": "Public"}], "methods": [{"name": "__init__", "args": ["self", "parent", "source"], "return_value": None, "encapsulation": "Public"}, {"name": "build", "args": ["self", "relationship", "target"], "return_value": None, "encapsulation": "Public"}]},
    {"name": "DrawIODiagram", "modules": ["uml_generator", "elements"], "relationships": [{"type": "inheritance", "related_module": ["base"], "related": "XmlElementFromString"}], "attributes": [{"name": "id", "data_type": None, "encapsulation": "Public"}, {"name": "default_parent_id", "data_type": None, "encapsulation": "Public"}], "methods": [{"name": "__init__", "args": ["self", "name"], "return_value": None, "encapsulation": "Public"}, {"name": "append", "args": ["self", "subelement"], "return_value": None, "encapsulation": "Public"}, {"name": "extend", "args": ["self", "elements"], "return_value": None, "encapsulation": "Public"}]},
    {"name": "UMLClassDiagramElement", "modules": ["uml_generator", "elements"], "relationships": [{"type": "inheritance", "related_module": ["xml", "etree", "ElementTree"], "related": "Element"}, {"type": "association", "related_module": ["uml_generator", "elements"], "related": "ClassHeader"}], "attributes": [{"name": "id", "data_type": None, "encapsulation": "Public"}, {"name": "_metadata", "data_type": None, "encapsulation": "Private"}, {"name": "_dimensions", "data_type": None, "encapsulation": "Private"}, {"name": "_parent", "data_type": None, "encapsulation": "Private"}], "methods": [{"name": "__init__", "args": ["self", "metadata", "dimensions", "parent"], "return_value": None, "encapsulation": "Public"}, {"name": "_build_class", "args": ["self"], "return_value": None, "encapsulation": "Private"}]},
    {"name": "ClassHeader", "modules": ["uml_generator", "elements"], "relationships": [{"type": "inheritance", "related_module": ["base"], "related": "XmlElementFromString"}], "attributes": [], "methods": [{"name": "__init__", "args": ["self", "name", "dimensions", "parent", "id"], "return_value": None, "encapsulation": "Public"}]},
    {"name": "ClassMethod", "modules": ["uml_generator", "elements"], "relationships": [{"type": "inheritance", "related_module": ["base"], "related": "XmlElementFromString"}], "attributes": [], "methods": [{"name": "__init__", "args": ["self", "dimensions", "encapsulation", "name", "args", "parent"], "return_value": None, "encapsulation": "Public"}]},
    {"name": "ClassStroke", "modules": ["uml_generator", "elements"], "relationships": [{"type": "inheritance", "related_module": ["base"], "related": "XmlElementFromString"}], "attributes": [], "methods": [{"name": "__init__", "args": ["self", "parent", "dimensions"], "return_value": None, "encapsulation": "Public"}]},
    {"name": "ClassAttribute", "modules": ["uml_generator", "elements"], "relationships": [{"type": "inheritance", "related_module": ["base"], "related": "XmlElementFromString"}], "attributes": [], "methods": [{"name": "__init__", "args": ["self", "parent", "encapsulation", "name", "data_type", "dimensions"], "return_value": None, "encapsulation": "Public"}]},
    {"name": "InheritanceRelationship", "modules": ["uml_generator", "relationships"], "relationships": [{"type": "inheritance", "related_module": ["base"], "related": "XmlElementFromString"}, {"type": "inheritance", "related_module": ["base"], "related": "UMLRelationship"}], "attributes": [], "methods": [{"name": "__init__", "args": ["self", "parent", "source", "target"], "return_value": None, "encapsulation": "Public"}]},
    {"name": "Dimensions", "modules": ["uml_generator", "utils"], "relationships": [{"type": "inheritance", "related_module": ["collections"], "related": "namedtuple('Dimensions', ['x', 'y', 'width', 'height'])"}, {"type": "association", "related_module": ["uml_generator", "utils"], "related": "Dimensions"}], "attributes": [{"name": "__slots__", "data_type": None, "encapsulation": "Public"}], "methods": [{"name": "__new__", "args": ["cls", "x", "y", "width", "height"], "return_value": None, "encapsulation": "Public"}]}
]

# Create a directed graph
G = nx.DiGraph()

# Add nodes
for cls in class_data:
    G.add_node(cls["name"], label=cls["name"])

# Add edges based on relationships
for cls in class_data:
    for rel in cls["relationships"]:
        related_class = rel.get("related")
        if related_class and related_class in G.nodes:
            if rel["type"] == "inheritance":
                G.add_edge(related_class, cls["name"], relationship="inheritance")
            elif rel["type"] == "association":
                G.add_edge(related_class, cls["name"], relationship="association")

# Use pydot layout
pos = pydot_layout(G, prog='dot')

# Define node size and color
node_size = 3000
node_color = 'lightblue'
edge_color = 'gray'

# Draw the graph
plt.figure(figsize=(15, 10))
nx.draw(G, pos=pos, with_labels=True, node_size=node_size, node_color=node_color, edge_color=edge_color, font_size=10, font_weight='bold', arrows=True)
plt.title("Class Diagram with Pydot Layout")
plt.show()

with open("position.txt", "w") as file:
    file.write(json.dumps(pos))