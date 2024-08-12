from pydiagram.uml_generator.base import UMLRelationship


class RelationshipBuilder:
    def __init__(self, parent: str, source: str):
        self.parent = parent
        self.source = source

    def build(self, relationship: UMLRelationship, target):
        return relationship(self.parent, self.source, target)
