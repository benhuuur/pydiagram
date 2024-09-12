import pydiagram.py_class_extractor.ast_management
import pydiagram.py_class_extractor.ast_collectors
import pydiagram.py_class_extractor.file_management
import pydiagram.py_class_extractor.schemas
import pydiagram.py_class_extractor.utils


def process_file(file_path: str, base_module_name: str) -> list:
    """
    Processes a single Python file to extract class metadata.

    Args:
        file_path (str): The path to the Python file.
        base_module_name (str): The base module name used for relative paths.

    Returns:
        list: A list of class metadata objects.
    """
    ast_tree = pydiagram.py_class_extractor.ast_management.parse_ast_from_file(
        file_path)
    class_nodes = pydiagram.py_class_extractor.ast_management.extract_class_nodes(
        ast_tree)
    modules = pydiagram.py_class_extractor.utils.extract_sublist_between(
        pydiagram.py_class_extractor.utils.split_path(
            file_path), base_module_name
    )

    import_aliases = pydiagram.py_class_extractor.ast_management.extract_alias_imports(
        ast_tree)

    classes_info = []
    for class_node in class_nodes:
        class_info = pydiagram.py_class_extractor.ast_management.get_class_metadata(
            class_node)
        class_info.modules = modules
        classes_info.append(class_info)

    for index, class_info in enumerate(classes_info):
        analyzer = pydiagram.py_class_extractor.ast_collectors.RelationshipInspector(
            import_aliases, classes_info)
        class_info.relationships = analyzer.visit(class_nodes[index])

    return classes_info


def generate_classes_dicts_from_file(file_path: str) -> None:
    """
    Analyzes the specified Python file and generates a JSON file containing class metadata.

    Args:
        file_path (str): The path to the Python file to be analyzed.
        output_path (str): The path to the output JSON file.
    """
    base_module_name = pydiagram.py_class_extractor.utils.split_path(
        file_path)[-1]
    class_metadata_list = process_file(file_path, base_module_name)

    # Convert class metadata to dictionary format
    class_metadata_dicts = [metadata.to_dictionary()
                            for metadata in class_metadata_list]

    return class_metadata_dicts


def generate_classes_dicts_from_directory(directory_path: str) -> None:
    """
    Analyzes all Python files in the specified directory and generates a JSON file with class metadata
    for all files combined.

    Args:
        directory_path (str): The path to the directory containing Python files.
        output_filename (str): The name of the output JSON file.
    """
    python_file_paths = pydiagram.py_class_extractor.file_management.find_files_with_extension(
        directory_path, ".py")
    base_module_name = pydiagram.py_class_extractor.utils.split_path(
        directory_path)[-1]

    # Collect metadata for all classes across all files
    all_class_metadata_list = []
    for file_path in python_file_paths:
        all_class_metadata_list.extend(
            process_file(file_path, base_module_name))

    for class_metadata in all_class_metadata_list:
        for relationship in class_metadata.relationships:
            if relationship.type == "association":
                continue

            flag = True
            for target_class_metadata in all_class_metadata_list:
                if relationship.related == target_class_metadata.name and bool(set(relationship.related_module) & set(target_class_metadata.modules)):
                    flag = False
            if flag:
                all_class_metadata_list.append(pydiagram.py_class_extractor.schemas.ClassInformation(
                    tuple(relationship.related_module), relationship.related, [], [], []))

    # Convert all class metadata to dictionary format
    all_class_metadata_dicts = [metadata.to_dictionary()
                                for metadata in all_class_metadata_list]

    return all_class_metadata_dicts
