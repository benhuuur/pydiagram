import ast
from pprint import pprint
from typing import List, Dict
from pydiagram.py_class_extractor import ast_collectors, file_management
from pydiagram.py_class_extractor.schemas import ClassInformation


def parse_ast_from_file(file_path: str) -> ast.AST:
    """
    Parses the given Python file and returns its abstract syntax tree (AST).

    Args:
        file_path (str): Path to the Python file.

    Returns:
        ast.AST: Abstract syntax tree representation of the parsed Python file.

    Raises:
        FileNotFoundError: If the file specified by `file_path` does not exist.
        SyntaxError: If there is an error in parsing the Python code.
        OSError: If there is a general operating system error while accessing `file_path`.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return ast.parse(file.read())
    except UnicodeDecodeError:
        encoding = file_management.detect_file_encoding(file_path)
        with open(file_path, "r", encoding=encoding) as file:
            return ast.parse(file.read())
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        raise
    except SyntaxError as e:
        print(f"Syntax error in file '{file_path}': {e}")
        raise
    except OSError as e:
        print(f"OS error while accessing file '{file_path}': {e}")
        raise


def display_ast_node(node: ast.AST):
    """
    Pretty prints the structure of the AST node.

    Args:
        node (ast.AST): Abstract syntax tree node representation of the Python code.
    """
    pprint(ast.dump(node, annotate_fields=True, indent=4))


def extract_class_nodes(tree: ast.AST) -> List[ast.ClassDef]:
    """
    Extracts ClassDef nodes from the AST.

    Args:
        tree (ast.AST): Abstract syntax tree of the Python code.

    Returns:
        List[ast.ClassDef]: List of ClassDef nodes found in the AST.
    """
    collector = ast_collectors.ClassDefCollector()
    collector.visit(tree)
    return collector.collected_classes


def extract_alias_imports(tree: ast.AST) -> Dict[str, str]:
    """
    Extracts import aliases from an Abstract Syntax Tree (AST) of Python code.

    Args:
        tree (ast.AST): Abstract syntax tree representing the Python code to be analyzed.

    Returns:
        Dict[str, str]: A dictionary where keys are import aliases and values are the original import names.
    """
    collector = ast_collectors.ImportCollector()
    collector.visit(tree)

    alias_inspector = ast_collectors.AliasInspector()
    for import_node in collector.import_nodes:
        alias_inspector.visit(import_node)

    return alias_inspector.alias_map


def get_class_metadata(class_node: ast.ClassDef) -> ClassInformation:
    """
    Retrieves metadata for a class node from an Abstract Syntax Tree (AST).

    Args:
        class_node (ast.ClassDef): The class node in the AST representing the class to analyze.

    Returns:
        ClassInformation: An object containing metadata about the class, including its methods and attributes.

    Raises:
        ValueError: If the provided class_node is not a valid ast.ClassDef instance.
    """
    if not isinstance(class_node, ast.ClassDef):
        raise ValueError("Provided class_node must be an instance of ast.ClassDef")

    inspector = ast_collectors.ClassMetadataInspector()
    class_metadata = inspector.visit(class_node)

    return class_metadata
