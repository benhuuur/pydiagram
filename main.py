from pydiagram import DrawioDiagramBuilder, ElementConfigManager, generate_classes_dicts_from_directory, generate_classes_dicts_from_file
import json


if __name__ == "__main__":
    # Find all Python files in a specified directory and its subdirectories
    target_directory = r"C:\Users\Aluno\Desktop\pydiagram\teste.py"
    classes_metadata = generate_classes_dicts_from_file(target_directory)
    # target_directory = r"C:\Users\Aluno\AppData\Local\Programs\Python\Python312\Lib\json"
    # classes_metadata = generate_classes_dicts_from_directory(target_directory)

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
    
    builder.edit_class()

    xml_diagram = builder.build()
    xml_diagram.write(r"output.xml", encoding="utf-8")