import networkx as nx
import matplotlib.pyplot as plt

def find(parent, node):
    # Función auxiliar para encontrar el conjunto al que pertenece un nodo
    if parent[node] == node:
        return node
    return find(parent, parent[node])

def union(parent, rank, node1, node2):
    # Función auxiliar para unir dos conjuntos por rango
    root1 = find(parent, node1)
    root2 = find(parent, node2)

    if rank[root1] < rank[root2]:
        parent[root1] = root2
    elif rank[root1] > rank[root2]:
        parent[root2] = root1
    else:
        parent[root2] = root1
        rank[root1] += 1

def kruskal(graph, maximum_cost=False):
    # Ordenar las aristas en orden ascendente (o descendente si maximum_cost=True)
    sorted_edges = sorted(graph.edges(data=True), key=lambda x: x[2]['weight'], reverse=maximum_cost)
    
    # Inicializar el árbol parcial y el diccionario de conjuntos disjuntos
    minimum_spanning_tree = nx.Graph()
    parent = {node: node for node in graph.nodes()}
    rank = {node: 0 for node in graph.nodes()}
    
    for edge in sorted_edges:
        node1, node2, data = edge
        weight = data['weight']
        
        # Verificar si las aristas conectan nodos de conjuntos disjuntos
        if find(parent, node1) != find(parent, node2):
            # Unir los conjuntos disjuntos y agregar la arista al árbol parcial
            union(parent, rank, node1, node2)
            minimum_spanning_tree.add_edge(node1, node2, weight=weight)
    
    return minimum_spanning_tree

# Ejemplo de grafo
graph = nx.Graph()
graph.add_edge('A', 'B', weight=4)
graph.add_edge('A', 'C', weight=2)
graph.add_edge('B', 'D', weight=5)
graph.add_edge('B', 'E', weight=1)
graph.add_edge('C', 'E', weight=3)
graph.add_edge('D', 'E', weight=2)

# Obtener el árbol de mínimo costo utilizando el algoritmo de Kruskal
minimum_spanning_tree = kruskal(graph)

# Obtener el árbol de máximo costo utilizando el algoritmo de Kruskal
maximum_spanning_tree = kruskal(graph, maximum_cost=True)

# Graficar el árbol de mínimo costo
pos = nx.spring_layout(minimum_spanning_tree)

plt.subplot(1, 2, 1)
nx.draw_networkx(minimum_spanning_tree, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=12)
edge_labels = nx.get_edge_attributes(minimum_spanning_tree, 'weight')
nx.draw_networkx_edge_labels(minimum_spanning_tree, pos, edge_labels=edge_labels)
plt.title('Árbol de Mínimo Costo')

# Graficar el árbol de máximo costo
plt.subplot(1, 2, 2)
nx.draw_networkx(maximum_spanning_tree, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=12)
edge_labels = nx.get_edge_attributes(maximum_spanning_tree, 'weight')
nx.draw_networkx_edge_labels(maximum_spanning_tree, pos, edge_labels=edge_labels)
plt.title('Árbol de Máximo Costo')

# Mostrar los árboles
plt.tight_layout()
plt.show()
