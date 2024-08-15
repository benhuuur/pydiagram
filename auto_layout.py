# import pydot
# import networkx as nx
# import matplotlib.pyplot as plt
# from networkx.drawing.nx_pydot import graphviz_layout

# # Criação de um grafo direcionado para representar classes e herança
# G = nx.DiGraph()

# # Adicionando nós (classes)
# G.add_node('Animal')
# G.add_node('Mammal')
# G.add_node('Bird')
# G.add_node('Dog')
# G.add_node('Cat')
# G.add_node('Parrot')
# G.add_node('Sparrow')

# # Adicionando arestas (herança e associações)
# G.add_edge('Animal', 'Mammal')
# G.add_edge('Animal', 'Bird')
# G.add_edge('Mammal', 'Dog')
# G.add_edge('Mammal', 'Cat')
# G.add_edge('Bird', 'Parrot')
# G.add_edge('Bird', 'Sparrow')

# # Usar o layout Graphviz para uma visualização hierárquica
# pos = graphviz_layout(G, prog='dot')

# # Desenhar o grafo
# plt.figure(figsize=(12, 10))
# nx.draw(G, pos, with_labels=True, node_size=3000, node_color='lightblue', font_size=12, font_weight='bold', arrows=True, node_shape='o', edge_color='gray', width=2, alpha=0.7)
# plt.title("Diagrama UML de Classes com Layout Hierárquico")
# plt.show()


import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout

G = nx.DiGraph()
# Adicionar nós e arestas
pos = graphviz_layout(G, prog='dot')
nx.draw(G, pos, with_labels=True)
plt.show()
