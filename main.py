import xml.etree.ElementTree as ET

from pydiagram.py_class_extractor import generate_classes_dicts_from_directory, generate_classes_dicts_from_file
from pydiagram.py_class_extractor.ast_management import parse_ast_from_file
from pydiagram.py_class_extractor.file_management import save_data_to_json
from pydiagram.uml_generator.builders.relationships import RelationshipBuilder
from pydiagram.uml_generator.elements import DrawIODiagram, UMLClassDiagramElement
from pydiagram.uml_generator.relationships import InheritanceRelationship
from pydiagram.uml_generator.utils import Dimensions

import json
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import pydot_layout
import pydot


def has_common_element(arr1, arr2):
    return bool(set(arr1) & set(arr2))


if __name__ == "__main__":
    ast = parse_ast_from_file(
        r"pydiagram\py_class_extractor\schemas.py")

    diagram = DrawIODiagram("pydiagram")
    metadata = generate_classes_dicts_from_file(
        r"C:\Users\Aluno\Desktop\pydiagram\teste.py")
    metadata = generate_classes_dicts_from_directory(
        r"C:\Users\Aluno\Desktop\pydiagram\pydiagram\uml_generator")
    save_data_to_json("class.json", metadata)

    G = nx.DiGraph()
    for cls in metadata:
        G.add_node(cls["name"], label=cls["name"])
        
    for cls in metadata:
        for rel in cls["relationships"]:
            related_class = rel.get("related")
            if related_class and related_class in G.nodes:
                if rel["type"] == "inheritance":
                    G.add_edge(related_class, cls["name"], relationship="inheritance")
                elif rel["type"] == "association":
                    G.add_edge(related_class, cls["name"], relationship="association")
    
    pos = pydot_layout(G, prog='dot')

    classes = list()
    for class_metadata in metadata:
        
        x = pos[class_metadata["name"]][0]*2
        y = pos[class_metadata["name"]][1]*4
        
        dimensions = Dimensions(x, y, 160, 26)
        UML_class = UMLClassDiagramElement(
            class_metadata, dimensions, diagram.default_parent_id)
        classes.append(UML_class)
        # x += 170

    relationships = list()
    for source_index, source_class_metadata in enumerate(metadata):
        for relationship in source_class_metadata["relationships"]:
            source_id = classes[source_index].id
            parent_id = diagram.default_parent_id
            builder = RelationshipBuilder(parent_id, source_id)
            continue
            if relationship["type"] == "inheritance":
                flag = True
                for target_index, target_class_metadata in enumerate(metadata):
                    if (relationship["related"] == target_class_metadata["name"]) and has_common_element(relationship["related_module"], target_class_metadata["modules"]):
                        relationships.append(builder.build(
                            InheritanceRelationship, classes[target_index].id))
                        flag = False
                        break
                if flag:
                    import_metadata = {
                        "modules": relationship["related_module"],
                        "name": relationship["related"],
                        "relationships": [],
                        "attributes": [],
                        "methods": []
                    }
                    metadata.append(import_metadata)
                    y = -100
                    dimensions = Dimensions(x, y, 160, 26)
                    import_class = UMLClassDiagramElement(
                        import_metadata, dimensions, diagram.default_parent_id)
                    classes.append(import_class)
                    relationships.append(builder.build(
                        InheritanceRelationship, import_class.id))
                    x += 170

    diagram.extend(relationships)
    diagram.extend(classes)
    with open('output.xml', 'w', encoding='utf-8') as file:
        file.write(ET.tostring(diagram, encoding='unicode'))
