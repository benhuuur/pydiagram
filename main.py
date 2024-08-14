import xml.etree.ElementTree as ET

from pydiagram.py_class_extractor import generate_classes_dicts_from_file, generate_classes_dicts_from_directory
from pydiagram.py_class_extractor.file_management import save_data_to_json
from pydiagram.uml_generator.builders.relationships import RelationshipBuilder
from pydiagram.uml_generator.elements import DrawIODiagram, UMLClassDiagramElement
from pydiagram.uml_generator.relationships import InheritanceRelationship
from pydiagram.uml_generator.utils import Dimensions

# from pydiagram.uml_generator import utils

if __name__ == "__main__":

    diagram = DrawIODiagram("pydiagram")
    metadata = generate_classes_dicts_from_directory(
        r"C:\Users\Aluno\Desktop\pydiagram")
    save_data_to_json("class.json", metadata)
    # with open('class.json', "r") as file:
    #     metadata = json.load(file)
    x = 0
    y = 0
    classes = list()
    for class_metadata in metadata:
        dimensions = Dimensions(x, y, 160, 26)
        UML_class = UMLClassDiagramElement(
            class_metadata, dimensions, diagram.default_parent_id)
        classes.append(UML_class)
        x += 170

    relationships = list()
    for source_index, source_class_metadata in enumerate(metadata):
        for relationship in source_class_metadata["relationships"]:
            source_id = classes[source_index].id
            parent_id = diagram.default_parent_id
            builder = RelationshipBuilder(parent_id, source_id)
            if relationship["type"] == "inheritance":
                flag = True
                for target_index, target_class_metadata in enumerate(metadata):
                    if relationship["related"] == target_class_metadata["name"]:
                        relationships.append(builder.build(
                            InheritanceRelationship, classes[target_index].id))
                        flag = False
                        break
                if flag:
                    import_metadata = {
                        "modules": [],
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
