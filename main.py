import logging
import os
import subprocess
import sys
import xml.etree.ElementTree as ET

from pydiagram.py_class_extractor import generate_classes_dicts_from_directory, generate_classes_dicts_from_file
from pydiagram.py_class_extractor.ast_management import parse_ast_from_file
from pydiagram.py_class_extractor.file_management import save_data_to_json
from pydiagram.uml_generator.builders.relationships import RelationshipBuilder
from pydiagram.uml_generator.elements import DrawIODiagram, UMLClassDiagramElement
from pydiagram.uml_generator.relationships import AssociationRelationship, InheritanceRelationship
from pydiagram.uml_generator.utils import Dimensions

import networkx as nx
from networkx.drawing.nx_pydot import pydot_layout

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def has_common_element(arr1, arr2):
    if len(arr1) == 0 and len(arr2) == 0:
        return True
    return bool(set(arr1) & set(arr2))


def install_graphviz():
    """Install Graphviz using winget if it's not already installed."""
    try:
        # Check if Graphviz is already installed
        result = subprocess.run(
            ['winget', 'list', 'Graphviz.Graphviz'], capture_output=True, text=True)
        if "Graphviz" in result.stdout:
            logging.info("Graphviz is already installed.")
            return
    except FileNotFoundError:
        logging.error("winget not found. Please install winget first.")
        sys.exit(1)
    except subprocess.CalledProcessError:
        logging.error("Error checking Graphviz installation status.")
        sys.exit(1)

    logging.info("Installing Graphviz...")
    try:
        subprocess.run([
            'winget', 'install', 'Graphviz.Graphviz',
            '--accept-source-agreements',
            '--accept-package-agreements'
        ], check=True)
        logging.info("Graphviz installed successfully.")
    except subprocess.CalledProcessError:
        logging.error("Failed to install Graphviz.")
        sys.exit(1)


def add_graphviz_to_path():
    """Add Graphviz to system PATH."""
    graphviz_bin_dir = r"C:\Program Files\Graphviz\bin"
    current_path = os.getenv('PATH', '')

    if graphviz_bin_dir not in current_path:
        new_path = os.pathsep.join([current_path, graphviz_bin_dir])
        os.environ['PATH'] = new_path

        try:
            subprocess.run(['setx', 'PATH', new_path], check=True)
            logging.info("Graphviz directory added to PATH.")
        except subprocess.CalledProcessError:
            logging.error("Failed to add Graphviz directory to PATH.")
            sys.exit(1)
    else:
        logging.info("Graphviz directory is already in PATH.")


def sanitize_class_name(name):
    """Sanitize class names to be used as node identifiers."""
    return ''.join(char for char in name if char.isalnum() or char == '_')


def autolayout_class_diagram(metadata):
    """Generate and save a class diagram from the metadata."""
    G = nx.DiGraph()
    for cls in metadata:
        sanitized_name = sanitize_class_name(cls["name"])
        G.add_node(sanitized_name, label=cls["name"])

    for cls in metadata:
        source_name = sanitize_class_name(cls["name"])
        for rel in cls["relationships"]:
            target_name = sanitize_class_name(rel.get("related", ""))
            if target_name in G.nodes:
                G.add_edge(source_name, target_name)

    pos = pydot_layout(G, prog='dot')
    return pos


def create_uml_classes(metadata, diagram, positions):
    """Create UML class elements from metadata."""
    classes = []
    for class_metadata in metadata:
        sanitized_name = sanitize_class_name(class_metadata["name"])
        if sanitized_name in positions:
            x, y = positions[sanitized_name]
            dimensions = Dimensions(x=x*3, y=y*5, width=160, height=26)
            UML_class = UMLClassDiagramElement(
                class_metadata, dimensions, diagram.default_parent_id)
            classes.append(UML_class)
        else:
            logging.warning(
                f"Node {class_metadata['name']} not found in positions.")
    return classes


def create_relationships(metadata, classes, diagram):
    """Create relationships between UML classes."""
    relationships = []
    for source_index, source_class_metadata in enumerate(metadata):
        source_id = classes[source_index].id
        for relationship in source_class_metadata["relationships"]:
            builder = RelationshipBuilder(diagram.default_parent_id, source_id)
            for target_index, target_class_metadata in enumerate(metadata):
                if (relationship["related"] == target_class_metadata["name"] and
                        has_common_element(relationship["modules"], target_class_metadata["modules"])):
                    if relationship["relation_type"] == "inheritance":
                        relationships.append(builder.build(
                            InheritanceRelationship, classes[target_index].id))
                    elif relationship["relation_type"] == "association":
                        relationships.append(builder.build(
                            AssociationRelationship, classes[target_index].id))
    return relationships


def main():
    install_graphviz()
    add_graphviz_to_path()

    metadata = generate_classes_dicts_from_file(
        r"C:\Users\Aluno\Desktop\pydiagram\tests\test_2.py")
    
    # metadata = generate_classes_dicts_from_directory(
    #     r"C:\Users\Aluno\Desktop\pydiagram\pydiagram")
    
    # metadata = generate_classes_dicts_from_directory(
    #     r"C:\Users\Aluno\AppData\Local\Programs\Python\Python312\Lib\json")
    
    save_data_to_json("class.json", metadata)

    positions = autolayout_class_diagram(metadata)

    diagram = DrawIODiagram("pydiagram")
    classes = create_uml_classes(metadata, diagram, positions)
    relationships = create_relationships(metadata, classes, diagram)

    diagram.extend(relationships)
    diagram.extend(classes)
    with open('output.xml', 'w', encoding='utf-8') as file:
        file.write(ET.tostring(diagram, encoding='unicode'))

    logging.info("UML diagram saved as 'output.xml'.")


if __name__ == "__main__":
    main()
