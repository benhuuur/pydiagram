import ast

from pydiagram.py_class_extractor.schemas import ClassInformation, FunctionInformation, AttributeInformation, RelationshipInformation


class ClassDefCollector(ast.NodeVisitor):
    """
    A NodeVisitor implementation to collect ClassDef nodes from AST.

    Attributes:
    - class_defs (list): List to store ClassDef nodes found during traversal.
    """

    def __init__(self) -> None:
        """
        Initializes an instance of ClassDefCollector.
        """
        self.class_defs = []

    def visit_ClassDef(self, node):
        """
        Visits a ClassDef node and appends it to the class_defs list.

        Args:
        - node (ast.ClassDef): ClassDef node to visit.
        """
        self.class_defs.append(node)
        self.generic_visit(node)


class ClassDefInspector(ast.NodeVisitor):
    """
    A NodeVisitor implementation to visit and analyze various nodes in AST and get metadata from the classes.

    Attributes:
    - current_class (ast.ClassDef or None): Current ClassDef node being visited.
    - current_function (ast.FunctionDef or None): Current function node being visited.
    - methods (list): List to store FunctionInfo objects representing methods.
    - attributes (list): List to store AttributeInfo objects representing attributes.
    """

    def __init__(self) -> None:
        """
        Initializes an instance of ClassInspector.
        """
        self.current_class: ast.ClassDef = None
        self.current_function: ast.FunctionDef = None
        self.current_assign: ast.AST = None
        self.methods = []
        self.attributes = []

    def visit_ClassDef(self, node: ast.ClassDef) -> ClassInformation:
        """
        Visits a ClassDef node and collects information about it.

        Args:
        - node (ast.ClassDef): ClassDef node to visit.

        Returns:
        - ClassInformation: Information about the visited class.
        """
        self.current_class = node
        self.generic_visit(node)

        class_info = ClassInformation(
            modules=None, name=node.name, relationships=None, methods=tuple(self.methods), attributes=tuple(self.attributes)
        )

        return class_info

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        """
        Visits a FunctionDef node and collects information about it.

        Args:
        - node (ast.FunctionDef): FunctionDef node to visit.

        Returns:
        - ast.FunctionDef: The visited function node.
        """
        args = [arg.arg for arg in node.args.args]
        function_name = node.name
        function_encapsulation = self._determine_encapsulation(function_name)

        self.methods.append(FunctionInformation(
            name=function_name, args=args, return_value=None, encapsulation=function_encapsulation
        ))

        self.current_function = node
        self.generic_visit(node)
        self.current_function = None

        return node

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> ast.AsyncFunctionDef:
        """
        Visits an AsyncFunctionDef node and collects information about it.

        Args:
        - node (ast.AsyncFunctionDef): AsyncFunctionDef node to visit.

        Returns:
        - ast.AsyncFunctionDef: The visited async function node.
        """
        args = [arg.arg for arg in node.args.args]

        self.methods.append(FunctionInformation(
            name=node.name, args=args, return_value=None, encapsulation="Public"
        ))

        self.current_function = node
        self.generic_visit(node)
        self.current_function = None

        return node

    def visit_AnnAssign(self, node: ast.AnnAssign) -> ast.AnnAssign:
        """
        Visits an AnnAssign node (annotation assignment) and collects attribute information.

        Args:
        - node (ast.AnnAssign): AnnAssign node to visit.

        Returns:
        - ast.AnnAssign: The visited AnnAssign node.
        """
        self.current_assign = node
        self.visit(node.target)
        self.current_assign = None

        return node

    def visit_Assign(self, node: ast.Assign) -> ast.Assign:
        """
        Visits an Assign node and collects attribute information.

        Args:
        - node (ast.Assign): Assign node to visit.

        Returns:
        - ast.Assign: The visited Assign node.
        """
        self.current_assign = node
        for target in node.targets:
            self.visit(target)
        self.current_assign = None

        return node

    def visit_Attribute(self, node: ast.Attribute) -> str:
        """
        Visits an Attribute node and retrieves the attribute name.

        Args:
        - node (ast.Attribute): Attribute node to visit.

        Returns:
        - str: The name of the visited attribute.
        """
        if isinstance(node.value, ast.Name):
            if self.current_assign and (self.current_function is None or
                (self.current_function.name == "__init__" and isinstance(self.current_assign, (ast.Assign, ast.AnnAssign)))):
                attribute_name = node.attr
                self.attributes.append(AttributeInformation(
                    name=attribute_name,
                    encapsulation=self._determine_encapsulation(
                        attribute_name),
                    data_type=None
                ))
            return node.attr

        return self.visit(node.value)

    def visit_Name(self, node: ast.Name) -> str:
        """
        Visits a Name node and retrieves the identifier.

        Args:
        - node (ast.Name): Name node to visit.

        Returns:
        - str: The identifier of the visited name.
        """
        if self.current_assign and (self.current_function is None or
            (self.current_function.name == "__init__" and isinstance(self.current_assign, ast.Attribute))):
            attribute_name = node.id
            self.attributes.append(AttributeInformation(
                name=attribute_name,
                encapsulation=self._determine_encapsulation(attribute_name),
                data_type=None
            ))

        return node.id

    def visit_Constant(self, node: ast.Constant) -> str:
        """
        Visits a Constant node and retrieves its value type.

        Args:
        - node (ast.Constant): Constant node to visit.

        Returns:
        - str: The type of the constant value.
        """
        return type(node.value).__name__

    def visit_Tuple(self, node: ast.Tuple) -> list:
        """
        Visits a Tuple node and retrieves its values.

        Args:
        - node (ast.Tuple): Tuple node to visit.

        Returns:
        - list: List of values in the tuple.
        """
        values = [self.visit(elt)
                             for elt in node.elts if self.visit(elt) is not None]
        return values

    def visit_arg(self, node: ast.arg) -> ast.arg:
        """
        Visits an arg node and returns it.

        Args:
        - node (ast.arg): arg node to visit.

        Returns:
        - ast.arg: The visited arg node.
        """
        return node  # Skip this node

    def _determine_encapsulation(self, name: str) -> str:
        """
        Determines the encapsulation level of a given name.

        Args:
        - name (str): The name to analyze.

        Returns:
        - str: The encapsulation level ("Public", "Private").
        """
        if name.startswith('__') and name.endswith('__'):
            return "Public"
        elif name.startswith('_'):
            return "Private"
        return "Public"


class RelationshipInspector(ast.NodeVisitor):
    def __init__(self, alias: dict) -> None:
        self.alias = alias if alias else dict()
        self.relationships = list()
        self.current_inheritance: ast.AST = None

    def visit_ClassDef(self, node: ast.ClassDef):
        """
        Visits a ClassDef node and analyzes its inheritance relationships.

        Args:
        - node (ast.ClassDef): The class definition node to visit.

        Returns:
        - tuple: A tuple of RelationshipInformation objects representing inheritance relationships.
        """
        for base in node.bases:
            self.current_inheritance = base
            inheritance = self.visit(base)
            if inheritance in self.alias.values():
                self.relationships.append(RelationshipInformation(
                    type="inheritance", related=self.alias[inheritance]
                ))
            else:
                self.relationships.append(RelationshipInformation(
                    type="inheritance", related=inheritance
                ))
            self.current_inheritance = None
        return tuple(self.relationships)

    def visit_Attribute(self, node: ast.Attribute) -> str:
        """
        Visits an Attribute node and retrieves its full name.

        Args:
        - node (ast.Attribute): The attribute node to visit.

        Returns:
        - str: The full name of the visited attribute.
        """
        if self.current_inheritance is not None:
            return f"{self.visit(node.value)}.{node.attr}"
        return node.attr  # Handle cases where current_inheritance is None.

    def visit_Subscript(self, node: ast.Subscript) -> str:
        """
        Visits a Subscript node and retrieves its string representation.

        Args:
        - node (ast.Subscript): The subscript node to visit.

        Returns:
        - str: String representation of the visited Subscript node.
        """
        return f"{self.visit(node.value)}[{self.visit(node.slice)}]"

    def visit_Name(self, node: ast.Name) -> str:
        """
        Visits a Name node and retrieves its identifier.

        Args:
        - node (ast.Name): The name node to visit.

        Returns:
        - str: The identifier of the visited name.
        """
        return node.id

    def visit_Call(self, node: ast.Call) -> str:
        """
        Visits a Call node and retrieves its function call representation.

        Args:
        - node (ast.Call): The call node to visit.

        Returns:
        - str: String representation of the function call.
        """
        function_name = self.visit(node.func)
        args = ", ".join(self.visit(arg) for arg in node.args)
        return f"{function_name}({args})"

    def visit_Constant(self, node: ast.Constant) -> str:
        """
        Visits a Constant node and retrieves its value.

        Args:
        - node (ast.Constant): The constant node to visit.

        Returns:
        - str: The value of the constant.
        """
        return str(node.value)

    def visit_Tuple(self, node: ast.Tuple) -> str:
        """
        Visits a Tuple node and retrieves its string representation.

        Args:
        - node (ast.Tuple): The tuple node to visit.

        Returns:
        - str: String representation of the visited Tuple node.
        """
        values = ", ".join(self.visit(elt) for elt in node.elts)
        return f"({values})"

    def visit_List(self, node: ast.List) -> str:
        values = ", ".join(self.visit(elt) for elt in node.elts)
        return f"({values})"


class ImportCollector(ast.NodeVisitor):
    def __init__(self) -> None:
        self.imports = list()

    def visit_Import(self, node: ast.Import) -> None:
        """
        Visits an Import node and adds it to the imports list.

        Args:
        - node (ast.Import): The Import node to visit.
        """
        self.imports.append(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """
        Visits an ImportFrom node and adds it to the imports list.

        Args:
        - node (ast.ImportFrom): The ImportFrom node to visit.
        """
        self.imports.append(node)


class AliasCollector(ast.NodeVisitor):
    def __init__(self) -> None:
        self.alias_import = dict()

    def visit_Import(self, node: ast.Import) -> None:
        """
        Visits an Import node and extracts aliases from it.

        Args:
        - node (ast.Import): The Import node to visit.
        """
        for name in node.names:
            alias_import = self.visit(name)
            if alias_import:
                self.alias_import.update(alias_import)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """
        Visits an ImportFrom node and extracts aliases from it.

        Args:
        - node (ast.ImportFrom): The ImportFrom node to visit.
        """
        for name in node.names:
            alias_import = self.visit(name)
            if alias_import:
                self.alias_import.update(alias_import)

    def visit_alias(self, node: ast.alias) -> dict:
        """
        Visits an alias node and retrieves its alias name and original name.

        Args:
        - node (ast.alias): The alias node to visit.

        Returns:
        - dict: A dictionary with the alias as the key and the original name as the value.
        """
        if node.asname:
            return {node.asname: node.name}