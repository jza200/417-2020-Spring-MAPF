import networkx as nx
G = nx.Graph()
G.add_node('A')
G.add_node('B')
G.add_edge('A', 'B')
print(G.edges)