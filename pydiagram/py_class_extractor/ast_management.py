import ast

from pprint import pprint
from typing import List
from pydiagram.py_class_extractor import ast_collectors
from pydiagram.py_class_extractor import file_management

from pydiagram.py_class_extractor.schemas import ClassInformation


def parse_ast_from_file(file_path: str) -> ast.AST:
    """
    Parses the given Python file and returns the abstract syntax tree (AST).

    Args:
    - file_path (str): Path to the Python file.

    Returns:
    - ast.AST: Abstract syntax tree representation of the parsed Python file.

    Raises:
    - FileNotFoundError: If the file specified by `file_path` does not exist.
    - SyntaxError: If there is an error in parsing the Python code.
    - OSError: If there is a general operating system error while accessing `file_path`.
    """
    try:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return ast.parse(file.read())
        except UnicodeDecodeError:
            with open(file_path, "r", encoding=file_management.detect_file_encoding(file_path)) as file:
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


def display_ast_node(node: ast.stmt):
    """
    Pretty prints the structure of the AST node.

    Args:
    - node: Abstract syntax tree node representation of the Python code.
    """
    pprint(ast.dump(node))


def extract_class_nodes(tree: ast.AST) -> List:
    """
    Extracts ClassDef nodes from the AST.

    Args:
    - tree (ast.AST): Abstract syntax tree of the Python code.

    Returns:
    - list: List of ClassDef nodes found in the AST.
    """
    collector = ast_collectors.ClassDefCollector()
    collector.visit(tree)
    return collector.class_defs


def extract_alias_imports(tree: ast.AST) -> dict:
    """
    Extracts import aliases from an Abstract Syntax Tree (AST) of Python code.

    This function uses an import collector to identify all import nodes
    in the AST and then applies a visitor to extract the aliases associated
    with those imports.

    The returned dictionary has aliases as keys and their original import values as the values.

    Parameters:
    ----------
    tree : ast.AST
        The Abstract Syntax Tree representing the Python code to be analyzed.

    Returns:
    -------
    dict
        A dictionary where the keys are import aliases and the values are the original import values.
    """
    collector = ast_collectors.ImportCollector()
    collector.visit(tree)
    imports = collector.imports

    visitor = ast_collectors.AliasInspector()
    for import_node in imports:
        visitor.visit(import_node)

    return visitor.alias_import


def  get_class_metadata(class_node: ast.ClassDef) -> ClassInformation:
    """
    Retrieves metadata for a class node from an Abstract Syntax Tree (AST).

    This function uses a visitor pattern to analyze the class node and extract
    its metadata, including relationships to other classes.

    Parameters:
    ----------
    class_node : ast.ClassDef
        The class node in the AST representing the class to analyze.

    alias : dict
        A dictionary representing aliases for the class, which may be used for
        further processing or identification.

    Returns:
    -------
    ClassInformation
        An object containing metadata about the class, including its relationships.

    Raises:
    ------
    ValueError
        If the provided class_node is not a valid class definition.
    """
    if not isinstance(class_node, ast.ClassDef):
        raise ValueError(
            "Provided class_node must be an instance of ast.ClassDef")

    visitor = ast_collectors.ClassDefInspector()
    current_class_data: ClassInformation = visitor.visit(class_node)

    return current_class_data
