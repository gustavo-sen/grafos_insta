import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict

# Inicialização do grafo
def criar_grafo(vertices):
    return defaultdict(list)

# Função para adicionar arestas ao grafo
def adicionar_aresta(grafo, u, v):
    grafo[u].append(v)

# Função auxiliar de DFS para preencher a pilha com a ordem de término
def dfs(grafo, v, visitado, pilha):
    visitado[v] = True
    for vizinho in grafo[v]:
        if not visitado[vizinho]:
            dfs(grafo, vizinho, visitado, pilha)
    pilha.append(v)

# Função para transpor o grafo
def transpor(grafo):
    grafo_transposto = criar_grafo(len(grafo))
    for i in grafo:
        for j in grafo[i]:
            adicionar_aresta(grafo_transposto, j, i)
    return grafo_transposto

# Função principal para encontrar componentes fortemente conectados
def kosaraju(grafo):
    pilha = []
    visitado = [False] * len(grafo)

    # Passo 1: Realizar DFS para preencher a pilha
    for i in range(len(grafo)):
        if not visitado[i]:
            dfs(grafo, i, visitado, pilha)

    # Passo 2: Transpor o grafo
    grafo_transposto = transpor(grafo)

    # Passo 3: Realizar DFS no grafo transposto na ordem dada pela pilha
    visitado = [False] * len(grafo)
    clusters = []

    while pilha:
        v = pilha.pop()
        if not visitado[v]:
            cluster = []
            dfs_cluster(grafo_transposto, v, visitado, cluster)
            clusters.append(cluster)

    return clusters

# Função auxiliar de DFS para marcar os componentes no grafo transposto
def dfs_cluster(grafo, v, visitado, cluster):
    visitado[v] = True
    cluster.append(v)
    for vizinho in grafo[v]:
        if not visitado[vizinho]:
            dfs_cluster(grafo, vizinho, visitado, cluster)

# Função para sugerir amigos baseando-se em amigos em comum
def sugerir_amigos(grafo, usuario):
    amigos = set(grafo[usuario])
    sugestoes = set()

    for amigo in amigos:
        for potencial in grafo[amigo]:
            if potencial != usuario and potencial not in amigos:
                sugestoes.add(potencial)

    return list(sugestoes)

# Criação do grafo usando dicionário
grafo = criar_grafo(7)

# Adicionando arestas (usuários seguem outros usuários)
arestas_dict = {
    0: [1],  # A segue B
    1: [2, 3],  # B segue C e D
    2: [0],  # C segue A
    3: [4],  # D segue E
    4: [5],  # E segue F
    5: [3, 6],  # F segue D e G
    6: [4]   # G segue E
}

# Adicionando as arestas ao grafo
for u, v_list in arestas_dict.items():
    for v in v_list:
        adicionar_aresta(grafo, u, v)

# Encontrando componentes fortemente conectados
clusters = kosaraju(grafo)

# Mostrando os clusters
print("Componentes fortemente conectados encontrados:")
for i, cluster in enumerate(clusters):
    print(f"Cluster {i + 1}: {cluster}")

# Sugerindo amigos para o usuário 0 (A)
sugestoes = sugerir_amigos(grafo, 0)
print(f"\nSugestões de amigos para o usuário 0: {sugestoes}")

# Visualizando o grafo
G = nx.DiGraph()
for u, v_list in arestas_dict.items():
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
plt.figure(figsize=(10, 7))
pos = nx.spring_layout(G)  # Layout para distribuir os nós
nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color="#A9A9A9", node_size=800, font_size=10, font_color="white", arrows=True)

# Adicionando arestas tracejadas para as sugestões
for usuario in sugestoes:
    plt.plot(*zip(pos[0], pos[usuario]), color='orange', linestyle='--', linewidth=2)  # Aresta tracejada de A para as sugestões

plt.title("Componentes Fortemente Conectados no Grafo")
plt.show()
