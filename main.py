# from pydiagram import DrawioDiagramBuilder, ElementConfigManager, generate_classes_dicts_from_directory, generate_classes_dicts_from_file
# import json


# if __name__ == "__main__":
#     # Find all Python files in a specified directory and its subdirectories
#     target_directory = r"C:\Users\Aluno\Desktop\pydiagram\teste.py"
#     classes_metadata = generate_classes_dicts_from_file(target_directory)
#     # target_directory = r"C:\Users\Aluno\AppData\Local\Programs\Python\Python312\Lib\json"
#     # classes_metadata = generate_classes_dicts_from_directory(target_directory)

#     ElementConfigManager(r'pydiagram\configs\elements.json')
#     manager = ElementConfigManager.get_manager()
    

#     # json_file = r'resources\json\class.json'

#     # with open(json_file, 'r', encoding='utf-8') as file:
#     #     classes_metadata = json.load(file)

#     builder = DrawioDiagramBuilder()
#     for index, metadata in enumerate(classes_metadata):
#         position = (0 + (index * 170), 0)

#         details = {
#             "position": position,
#             "class": metadata,
#             "width": 160,
#             "height": None
#         }

#         builder.append_class(details)
    
#     builder.edit_class()

#     xml_diagram = builder.build()
#     xml_diagram.write(r"output.xml", encoding="utf-8")

import xml.etree.ElementTree as ET

# Your original XML data without a parent
xml_content = """
<mxCell id="DFD5oipk4ANFZEnpcnx_-1" value="Classname"
    style="swimlane;fontStyle=1;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=26;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;whiteSpace=wrap;html=1;"
    parent="1" vertex="1">
    <mxGeometry x="10" y="10" width="160" height="86" as="geometry" />
</mxCell>
<mxCell id="DFD5oipk4ANFZEnpcnx_-2" value="+ field: type"
    style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=top;spacingLeft=4;spacingRight=4;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;whiteSpace=wrap;html=1;"
    parent="DFD5oipk4ANFZEnpcnx_-1" vertex="1">
    <mxGeometry y="26" width="160" height="26" as="geometry" />
</mxCell>
<mxCell id="DFD5oipk4ANFZEnpcnx_-3" value=""
    style="line;strokeWidth=1;fillColor=none;align=left;verticalAlign=middle;spacingTop=-1;spacingLeft=3;spacingRight=3;rotatable=0;labelPosition=right;points=[];portConstraint=eastwest;strokeColor=inherit;"
    parent="DFD5oipk4ANFZEnpcnx_-1" vertex="1">
    <mxGeometry y="52" width="160" height="8" as="geometry" />
</mxCell>
<mxCell id="DFD5oipk4ANFZEnpcnx_-4" value="+ method(type): type"
    style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=top;spacingLeft=4;spacingRight=4;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;whiteSpace=wrap;html=1;"
    parent="DFD5oipk4ANFZEnpcnx_-1" vertex="1">
    <mxGeometry y="60" width="160" height="26" as="geometry" />
</mxCell>
"""

import xml.etree.ElementTree as ET

# Exemplo de XML
xml_data = '''
<root>
    <parent>
        <child id="1">Value1</child>
        <child id="2">Value2</child>
    </parent>
</root>
'''

root = ET.fromstring(xml_data)

# Encontrar o elemento que queremos remover do pai
element_to_remove = root.find(".//child[@id='1']")

# Função para encontrar o pai do elemento
def find_parent(root, element):
    for parent in root.iter():
        if element in parent:
            return parent
    return None

# Encontrar o pai do elemento
parent = find_parent(root, element_to_remove)

# Se o elemento foi encontrado
if element_to_remove is not None and parent is not None:
    # Remover o elemento do pai
    parent.remove(element_to_remove)
    
    # Adicionar o elemento removido a um novo local, se necessário
    # Exemplo: adicionar ao elemento root (ou qualquer outro local)
    root.append(element_to_remove)
    
    # Imprimir o resultado
    new_xml = ET.tostring(root, encoding='unicode')
    print(new_xml)
else:
    print("Elemento ou pai não encontrado")

# class CustomElement(ET.Element):
    def append(self, obj):
        if isinstance(obj, MyCustomElements):
            obj.append_elements(self)
        else:
            super().append(obj)

