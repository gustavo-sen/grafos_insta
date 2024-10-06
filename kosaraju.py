import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.cm as cm
from graph_tool import *


# Criação do grafo usando dicionário
grafo = criar_grafo()

# Criação do grafo usando dicionário
arestas = {
    0: [1],  # A segue B
    1: [2, 3],  # B segue C e D
    2: [0],  # C segue A
    3: [4],  # D segue E
    4: [5],  # E segue F
    5: [3, 6],  # F segue D e G
    6: [4]   # G segue E
}

# Adicionando as arestas ao grafo
for u, v_list in arestas.items():
    for v in v_list:
        adicionar_aresta(grafo, u, v)

# Encontrando componentes fortemente conectados
clusters = kosaraju(grafo)

# Mostrando os clusters
print("Componentes fortemente conectados encontrados:")
for i, cluster in enumerate(clusters):
    print(f"Cluster {i + 1}: {cluster}")


# Visualizando o grafo
G = nx.DiGraph()
for u, v_list in arestas.items():
    for v in v_list:
        G.add_edge(u, v)

# Definindo cores para os componentes fortemente conectados
cores = ["#FF6347", "#4682B4", "#32CD32", "#FFD700", "#8A2BE2", "#FF69B4", "#00CED1"]
node_colors = []

# Mapeando os clusters para as cores
node_cluster_map = {}
for idx, cluster in enumerate(clusters):
    for node in cluster:
        node_cluster_map[node] = cores[idx % len(cores)]


# Atribuindo cores aos nós
for node in G.nodes():
    node_colors.append(node_cluster_map.get(node, "#000000"))

# Desenhando o grafo
plt.figure(figsize=(6, 5))
pos = nx.spring_layout(G)  # Layout para distribuir os nós
nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color="#A9A9A9", node_size=800, font_size=10, font_color="white", arrows=True)
plt.title("Componentes Fortemente Conectados no Grafo")
plt.show()


# Criando um grafo apenas com as sugestões de amizade
G_sugestoes = nx.DiGraph()

# Paleta de cores para sugestões de amizade
n_nodes = len(grafo)
colors = cm.get_cmap('tab10', n_nodes)  # Utiliza um mapa de cores com uma paleta discreta

print(f"cores: {colors}")
# Adicionando as sugestões de amizade ao grafo e definindo suas cores
edge_colors = []
for i in range(len(grafo)):
    sugestoes = sugerir_amigos(grafo, i, clusters)
    for usuario in sugestoes:
        G_sugestoes.add_edge(i, usuario)
        edge_colors.append(colors(i))
        
# Visualizando o grafo apenas com as sugestões de amizade
plt.figure(figsize=(6, 5))
nx.draw(G_sugestoes, pos, with_labels=True, node_color=node_colors, edge_color= edge_colors, node_size=800, font_size=10, font_color="white", arrows=True)
plt.title("Grafo com Sugestões de Amizade")
plt.show()

visualizar_sugestoes_para_no(0,grafo,clusters,pos)