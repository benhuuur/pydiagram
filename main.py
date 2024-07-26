from class_diagram_builder import class_structure_collector, file_management, ast_management
from pydiagram import DrawioDiagramBuilder, ElementConfigManager
import json


if __name__ == "__main__":
    # Find all Python files in a specified directory and its subdirectories
    target_directory = r"C:\Users\Aluno\AppData\Local\Programs\Python\Python312\Lib\json"
    python_files = file_management.find_files_with_extension(
        target_directory, ".py")

    print(python_files)

    class_data_list = []
    for file_path in python_files:
        ast_tree = ast_management.parse_ast_from_file(file_path)
        class_nodes = ast_management.extract_class_nodes(ast_tree)
        print(file_path)
        for class_node in class_nodes:
            visitor = class_structure_collector.ClassNodeVisitor()
            class_data_list.append(visitor.visit(class_node))

    classes_metadata = [current_class.to_dictionary()
                   for current_class in class_data_list]

    # file_management.save_data_to_json(
    #     data=classes_metadata, filename=r"class.json"
    # )

    ElementConfigManager(r'pydiagram\configs\elements.json')
    manager = ElementConfigManager.get_manager()

    # json_file = r'resources\json\class.json'

    # with open(json_file, 'r', encoding='utf-8') as file:
    #     classes_metadata = json.load(file)

    builder = DrawioDiagramBuilder()
    for index, metadata in enumerate(classes_metadata):
        position = (0 + (index * 170), 0)

        details = {
            "position": position,
            "class": metadata,
            "width": 160,
            "height": None
        }

        builder.append_class(details)

    xml_diagram = builder.build()
    xml_diagram.write(r"output.xml", encoding="utf-8")