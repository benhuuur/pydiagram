import pydiagram.py_class_extractor.ast_management as ast_mgmt
import pydiagram.py_class_extractor.ast_collectors as ast_collectors
import pydiagram.py_class_extractor.file_management as file_mgmt
import pydiagram.py_class_extractor.schemas as schemas
import pydiagram.py_class_extractor.utils as utils


def process_file(file_path: str, base_module_name: str) -> list:
    """
    Processes a single Python file to extract class metadata.

    Args:
        file_path (str): The path to the Python file.
        base_module_name (str): The base module name used for relative paths.

    Returns:
        list: A list of class metadata objects.
    """
    # Parse the abstract syntax tree (AST) from the file
    ast_tree = ast_mgmt.parse_ast_from_file(file_path)

    # Extract class nodes and module paths
    class_nodes = ast_mgmt.extract_class_nodes(ast_tree)
    module_paths = utils.extract_sublist_between(
        utils.split_path(file_path), base_module_name
    )
    import_aliases = ast_mgmt.extract_alias_imports(ast_tree)

    class_metadata_list = []
    for node in class_nodes:
        metadata = ast_mgmt.get_class_metadata(node)
        metadata.modules = module_paths
        class_metadata_list.append(metadata)

    # Analyze class relationships
    relationship_analyzer = ast_collectors.ClassRelationshipInspector(
        import_aliases, class_metadata_list)
    for index, metadata in enumerate(class_metadata_list):
        metadata.relationships = relationship_analyzer.visit(
            class_nodes[index])

    return class_metadata_list


def generate_classes_dicts_from_file(file_path: str) -> list:
    """
    Analyzes the specified Python file and returns class metadata in dictionary format.

    Args:
        file_path (str): The path to the Python file to be analyzed.

    Returns:
        list: A list of dictionaries representing class metadata.
    """
    base_module_name = utils.split_path(file_path)[-1]
    class_metadata_list = process_file(file_path, base_module_name)

    all_class_names = {
    metadata.name for metadata in class_metadata_list}
    for metadata in class_metadata_list:
        for relationship in metadata.relationships:
            if relationship.relation_type != "association" and relationship.related not in all_class_names:
                class_metadata_list.append(schemas.ClassInformation(
                    tuple(relationship.modules), relationship.related, [], [], []
                ))
                all_class_names.add(relationship.related)
                
    # Convert class metadata to dictionary format
    class_metadata_dicts = [metadata.to_dictionary()
                            for metadata in class_metadata_list]
    

    return class_metadata_dicts


def generate_classes_dicts_from_directory(directory_path: str) -> list:
    """
    Analyzes all Python files in the specified directory and returns a list of dictionaries
    containing class metadata for all files combined.

    Args:
        directory_path (str): The path to the directory containing Python files.

    Returns:
        list: A list of dictionaries representing class metadata.
    """
    python_file_paths = file_mgmt.find_files_with_extension(
        directory_path, ".py")
    base_module_name = utils.split_path(directory_path)[-1]

    # Collect metadata for all classes across all files
    combined_class_metadata_list = []
    for file_path in python_file_paths:
        combined_class_metadata_list.extend(
            process_file(file_path, base_module_name))

    # Ensure all relationships are accounted for
    all_class_names = {
        metadata.name for metadata in combined_class_metadata_list}
    for metadata in combined_class_metadata_list:
        for relationship in metadata.relationships:
            if relationship.relation_type != "association" and relationship.related not in all_class_names:
                combined_class_metadata_list.append(schemas.ClassInformation(
                    tuple(relationship.modules), relationship.related, [], [], []
                ))
                all_class_names.add(relationship.related)

    # Convert all class metadata to dictionary format
    combined_class_metadata_dicts = [
        metadata.to_dictionary() for metadata in combined_class_metadata_list]

    return combined_class_metadata_dicts
