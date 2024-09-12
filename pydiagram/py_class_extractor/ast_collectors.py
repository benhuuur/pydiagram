import ast
from typing import List, Dict, Union, Tuple
from pydiagram.py_class_extractor.schemas import ClassInformation, FunctionInformation, AttributeInformation, RelationshipInformation

class ClassDefCollector(ast.NodeVisitor):
    """
    Collects ClassDef nodes from the AST.

    Attributes:
    - collected_classes (List[ast.ClassDef]): List of ClassDef nodes found during traversal.
    """

    def __init__(self) -> None:
        """
        Initializes the ClassDefCollector.
        """
        self.collected_classes: List[ast.ClassDef] = []

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """
        Visits a ClassDef node and adds it to the collected_classes list.

        Args:
        - node (ast.ClassDef): The ClassDef node to visit.
        """
        self.collected_classes.append(node)
        self.generic_visit(node)


class ClassMetadataInspector(ast.NodeVisitor):
    """
    Analyzes nodes in the AST to extract metadata from classes.

    Attributes:
    - current_class (Union[ast.ClassDef, None]): The current ClassDef node being analyzed.
    - current_function (Union[ast.FunctionDef, None]): The current function node being analyzed.
    - current_assignment (Union[ast.AST, None]): The current assignment node being analyzed.
    - methods (List[FunctionInformation]): List of method information collected.
    - attributes (List[AttributeInformation]): List of attribute information collected.
    """

    def __init__(self) -> None:
        """
        Initializes the ClassMetadataInspector.
        """
        self.current_class: Union[ast.ClassDef, None] = None
        self.current_function: Union[ast.FunctionDef, None] = None
        self.current_assignment: Union[ast.AST, None] = None
        self.methods: List[FunctionInformation] = []
        self.attributes: List[AttributeInformation] = []

    def visit_ClassDef(self, node: ast.ClassDef) -> ClassInformation:
        """
        Visits a ClassDef node to extract class metadata.

        Args:
        - node (ast.ClassDef): The ClassDef node to visit.

        Returns:
        - ClassInformation: Metadata about the visited class, including methods and attributes.
        """
        self.current_class = node
        self.generic_visit(node)

        return ClassInformation(
            modules=None,
            name=node.name,
            relationships=None,
            methods=tuple(self.methods),
            attributes=tuple(self.attributes)
        )

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        """
        Visits a FunctionDef node to collect method information.

        Args:
        - node (ast.FunctionDef): The FunctionDef node to visit.

        Returns:
        - ast.FunctionDef: The visited FunctionDef node.
        """
        args = [arg.arg for arg in node.args.args]
        function_name = node.name
        encapsulation = self._get_encapsulation_level(function_name)

        self.methods.append(FunctionInformation(
            name=function_name,
            args=args,
            return_value=None,
            encapsulation=encapsulation
        ))

        self.current_function = node
        self.generic_visit(node)
        self.current_function = None

        return node

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> ast.AsyncFunctionDef:
        """
        Visits an AsyncFunctionDef node to collect async method information.

        Args:
        - node (ast.AsyncFunctionDef): The AsyncFunctionDef node to visit.

        Returns:
        - ast.AsyncFunctionDef: The visited AsyncFunctionDef node.
        """
        args = [arg.arg for arg in node.args.args]
        self.methods.append(FunctionInformation(
            name=node.name,
            args=args,
            return_value=None,
            encapsulation="Public"
        ))

        self.current_function = node
        self.generic_visit(node)
        self.current_function = None

        return node

    def visit_AnnAssign(self, node: ast.AnnAssign) -> ast.AnnAssign:
        """
        Visits an AnnAssign node (annotation assignment) to collect attribute information.

        Args:
        - node (ast.AnnAssign): The AnnAssign node to visit.

        Returns:
        - ast.AnnAssign: The visited AnnAssign node.
        """
        self.current_assignment = node
        self.visit(node.target)
        self.current_assignment = None

        return node

    def visit_Assign(self, node: ast.Assign) -> ast.Assign:
        """
        Visits an Assign node to collect attribute information.

        Args:
        - node (ast.Assign): The Assign node to visit.

        Returns:
        - ast.Assign: The visited Assign node.
        """
        self.current_assignment = node
        for target in node.targets:
            self.visit(target)
        self.current_assignment = None

        return node

    def visit_Attribute(self, node: ast.Attribute) -> str:
        """
        Visits an Attribute node to retrieve and process attribute names.

        Args:
        - node (ast.Attribute): The Attribute node to visit.

        Returns:
        - str: The name of the attribute.
        """
        if isinstance(node.value, ast.Name):
            if self._is_valid_attribute_assignment():
                attribute_name = node.attr
                self.attributes.append(AttributeInformation(
                    name=attribute_name,
                    encapsulation=self._get_encapsulation_level(attribute_name),
                    data_type=None
                ))
            return node.attr

        return self.visit(node.value)

    def visit_Name(self, node: ast.Name) -> str:
        """
        Visits a Name node to retrieve identifiers and process attributes.

        Args:
        - node (ast.Name): The Name node to visit.

        Returns:
        - str: The identifier of the name.
        """
        if self._is_valid_attribute_assignment():
            attribute_name = node.id
            self.attributes.append(AttributeInformation(
                name=attribute_name,
                encapsulation=self._get_encapsulation_level(attribute_name),
                data_type=None
            ))

        return node.id

    def visit_Constant(self, node: ast.Constant) -> str:
        """
        Visits a Constant node to determine its type.

        Args:
        - node (ast.Constant): The Constant node to visit.

        Returns:
        - str: The type of the constant value.
        """
        return type(node.value).__name__

    def visit_Tuple(self, node: ast.Tuple) -> List[Union[str, int, float, bool, None]]:
        """
        Visits a Tuple node to retrieve its values.

        Args:
        - node (ast.Tuple): The Tuple node to visit.

        Returns:
        - list: A list of values within the tuple.
        """
        return [self.visit(element) for element in node.elts if self.visit(element) is not None]

    def visit_arg(self, node: ast.arg) -> ast.arg:
        """
        Visits an arg node and returns it (currently does nothing).

        Args:
        - node (ast.arg): The arg node to visit.

        Returns:
        - ast.arg: The arg node.
        """
        return node  # No processing needed for args

    def _get_encapsulation_level(self, name: str) -> str:
        """
        Determines the encapsulation level of a given name.

        Args:
        - name (str): The name to analyze.

        Returns:
        - str: The encapsulation level ("Public" or "Private").
        """
        if name.startswith('__') and name.endswith('__'):
            return "Public"
        elif name.startswith('_'):
            return "Private"
        return "Public"

    def _is_valid_attribute_assignment(self) -> bool:
        """
        Checks if the current context is a valid attribute assignment.

        Returns:
        - bool: True if the current context is valid for attribute assignment.
        """
        return self.current_assignment and (
            self.current_function is None or
            (self.current_function.name == "__init__" and isinstance(
                self.current_assignment, (ast.Assign, ast.AnnAssign)))
        )


class ClassRelationshipInspector(ast.NodeVisitor):
    """
    Analyzes class relationships and associations in the AST.

    Attributes:
    - current_class_node (Union[ast.ClassDef, None]): The current ClassDef node being analyzed.
    - alias_map (Dict[str, str]): Map of alias names to original names.
    - relationships (List[RelationshipInformation]): List of relationships found during traversal.
    - current_base_node (Union[ast.AST, None]): The current base node being analyzed.
    - class_info_list (List[RelationshipInformation]): List of class information for resolving relationships.
    """

    def __init__(self, alias_map: Dict[str, str], class_info_list: List[RelationshipInformation]) -> None:
        """
        Initializes the ClassRelationshipInspector.

        Args:
        - alias_map (Dict[str, str]): Map of alias names to original names.
        - class_info_list (List[RelationshipInformation]): List of class information for resolving relationships.
        """
        self.current_class_node = None
        self.alias_map = alias_map or {}
        self.relationships: List[RelationshipInformation] = []
        self.current_base_node: Union[ast.AST, None] = None
        self.class_info_list = class_info_list

    def visit_ClassDef(self, node: ast.ClassDef) -> Tuple[RelationshipInformation, ...]:
        """
        Visits a ClassDef node and analyzes its inheritance relationships.

        Args:
        - node (ast.ClassDef): The class definition node to visit.

        Returns:
        - tuple: A tuple of RelationshipInformation objects representing inheritance relationships.
        """
        self.current_class_node = node

        for base in node.bases:
            self.current_base_node = base
            base_name = self.visit(base)
            resolved_base_name = self._resolve_aliases(base_name)
            base_parts = resolved_base_name.split(".")
            base_class_name = base_parts[-1]
            base_modules = base_parts[:-1]

            if any(info.name == base_class_name for info in self.class_info_list):
                for info in self.class_info_list:
                    if info.name == base_class_name:
                        self.relationships.append(RelationshipInformation(
                            relation_type="inheritance",
                            name=info.name,
                            modules=info.modules
                        ))
                        break
            else:
                self.relationships.append(RelationshipInformation(
                    relation_type="inheritance",
                    name=base_class_name,
                    modules=base_modules
                ))

            self.current_base_node = None

        self.generic_visit(node)
        return tuple(self.relationships)

    def visit_AnnAssign(self, node: ast.AnnAssign) -> ast.AnnAssign:
        """
        Visits an AnnAssign node to check for associations.

        Args:
        - node (ast.AnnAssign): The AnnAssign node to visit.

        Returns:
        - ast.AnnAssign: The visited AnnAssign node.
        """
        annotation = self.visit(node.annotation)
        resolved_annotation = self._resolve_aliases(annotation)

        for info in self.class_info_list:
            if info.name in resolved_annotation and self.current_class_node.name != info.name:
                self.relationships.append(RelationshipInformation(
                    relation_type="association",
                    name=info.name,
                    modules=info.modules
                ))

        return node

    def visit_Attribute(self, node: ast.Attribute) -> str:
        """
        Visits an Attribute node and returns its string representation.

        Args:
        - node (ast.Attribute): The Attribute node to visit.

        Returns:
        - str: The string representation of the attribute.
        """
        return ast.unparse(node)

    def visit_Subscript(self, node: ast.Subscript) -> str:
        """
        Visits a Subscript node and returns its string representation.

        Args:
        - node (ast.Subscript): The Subscript node to visit.

        Returns:
        - str: The string representation of the subscript.
        """
        return ast.unparse(node)

    def visit_Name(self, node: ast.Name) -> str:
        """
        Visits a Name node and returns its string representation.

        Args:
        - node (ast.Name): The Name node to visit.

        Returns:
        - str: The string representation of the name.
        """
        return ast.unparse(node)

    def visit_Call(self, node: ast.Call) -> str:
        """
        Visits a Call node to check for associations.

        Args:
        - node (ast.Call): The Call node to visit.

        Returns:
        - str: The string representation of the call.
        """
        if self.current_base_node:
            return ast.unparse(node)

        for arg in node.args:
            self.visit(arg)

        function_name = self.visit(node.func)
        if isinstance(function_name, str):
            resolved_function_name = self._resolve_aliases(function_name)
            for info in self.class_info_list:
                if info.name in resolved_function_name and self.current_class_node.name != info.name:
                    self.relationships.append(RelationshipInformation(
                        relation_type="association",
                        name=info.name,
                        modules=info.modules
                    ))

        return node

    def visit_BinOp(self, node: ast.BinOp) -> str:
        """
        Visits a BinOp node and returns its string representation.

        Args:
        - node (ast.BinOp): The BinOp node to visit.

        Returns:
        - str: The string representation of the binary operation.
        """
        return ast.unparse(node)

    def visit_Constant(self, node: ast.Constant) -> str:
        """
        Visits a Constant node and returns its string representation.

        Args:
        - node (ast.Constant): The Constant node to visit.

        Returns:
        - str: The string representation of the constant.
        """
        return ast.unparse(node)

    def visit_Tuple(self, node: ast.Tuple) -> str:
        """
        Visits a Tuple node and returns its string representation.

        Args:
        - node (ast.Tuple): The Tuple node to visit.

        Returns:
        - str: The string representation of the tuple.
        """
        return ast.unparse(node)

    def visit_List(self, node: ast.List) -> str:
        """
        Visits a List node and returns its string representation.

        Args:
        - node (ast.List): The List node to visit.

        Returns:
        - str: The string representation of the list.
        """
        return ast.unparse(node)

    def visit_arg(self, node: ast.arg) -> ast.arg:
        """
        Visits an arg node and checks for associations.

        Args:
        - node (ast.arg): The arg node to visit.

        Returns:
        - ast.arg: The arg node.
        """
        if node.annotation:
            annotation_str = self.visit(node.annotation)
            resolved_annotation = self._resolve_aliases(annotation_str)
            for info in self.class_info_list:
                if info.name in resolved_annotation and self.current_class_node.name != info.name:
                    self.relationships.append(RelationshipInformation(
                        relation_type="association",
                        name=info.name,
                        modules=info.modules
                    ))

        return node

    def _resolve_aliases(self, qualified_name: str) -> str:
        """
        Resolves aliases in a qualified name using the alias map.

        Args:
        - qualified_name (str): The qualified name to resolve.

        Returns:
        - str: The resolved name with aliases replaced.
        """
        for alias, original in self.alias_map.items():
            qualified_name = qualified_name.replace(alias, original)
        return qualified_name


class ImportCollector(ast.NodeVisitor):
    """
    Collects import statements from the AST.

    Attributes:
    - import_nodes (List[ast.AST]): List of import nodes found during traversal.
    """

    def __init__(self) -> None:
        """
        Initializes the ImportCollector.
        """
        self.import_nodes: List[ast.AST] = []

    def visit_Import(self, node: ast.Import) -> None:
        """
        Visits an Import node and adds it to the import_nodes list.

        Args:
        - node (ast.Import): The Import node to visit.
        """
        self.import_nodes.append(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """
        Visits an ImportFrom node and adds it to the import_nodes list.

        Args:
        - node (ast.ImportFrom): The ImportFrom node to visit.
        """
        self.import_nodes.append(node)


class AliasInspector(ast.NodeVisitor):
    """
    Inspects import statements to create a map of aliases to original names.

    Attributes:
    - alias_map (Dict[str, str]): Map of alias names to original names.
    """

    def __init__(self) -> None:
        """
        Initializes the AliasInspector.
        """
        self.alias_map: Dict[str, str] = {}

    def visit_Import(self, node: ast.Import) -> None:
        """
        Visits an Import node to extract aliases and updates the alias_map.

        Args:
        - node (ast.Import): The Import node to visit.
        """
        for alias_node in node.names:
            alias_mapping = self._extract_aliases(alias_node)
            self.alias_map.update(alias_mapping)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """
        Visits an ImportFrom node to extract aliases and updates the alias_map.

        Args:
        - node (ast.ImportFrom): The ImportFrom node to visit.
        """
        for alias_node in node.names:
            alias_mapping = self._extract_aliases(alias_node)
            if node.module:
                alias_mapping = {key: f"{node.module}.{value}" for key, value in alias_mapping.items()}
            self.alias_map.update(alias_mapping)

    def _extract_aliases(self, alias_node: ast.alias) -> Dict[str, str]:
        """
        Extracts alias mappings from an alias node.

        Args:
        - alias_node (ast.alias): The alias node to extract from.

        Returns:
        - Dict[str, str]: A dictionary mapping alias names to original names.
        """
        if alias_node.asname:
            return {alias_node.asname: alias_node.name}
        return {alias_node.name: alias_node.name}
