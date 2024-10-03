import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict

class Grafo:
    def __init__(self, vertices):
        self.vertices = vertices
        self.grafo = defaultdict(list)

    # Função para adicionar arestas ao grafo
    def adicionar_aresta(self, u, v):
        self.grafo[u].append(v)

    # Função auxiliar de DFS para preencher a pilha com a ordem de término
    def dfs(self, v, visitado, pilha):
        visitado[v] = True
        for vizinho in self.grafo[v]:
            if not visitado[vizinho]:
                self.dfs(vizinho, visitado, pilha)
        pilha.append(v)

    # Função para transpor o grafo
    def transpor(self):
        grafo_transposto = Grafo(self.vertices)
        for i in self.grafo:
            for j in self.grafo[i]:
                grafo_transposto.adicionar_aresta(j, i)
        return grafo_transposto

    # Função principal para encontrar componentes fortemente conectados
    def kosaraju(self):
        pilha = []
        visitado = [False] * self.vertices

        # Passo 1: Realizar DFS para preencher a pilha com a ordem de término dos nós
        for i in range(self.vertices):
            if not visitado[i]:
                self.dfs(i, visitado, pilha)

        # Passo 2: Transpor o grafo
        grafo_transposto = self.transpor()

        # Passo 3: Realizar DFS no grafo transposto na ordem dada pela pilha
        visitado = [False] * self.vertices
        clusters = []

        while pilha:
            v = pilha.pop()
            if not visitado[v]:
                cluster = []
                grafo_transposto.dfs_cluster(v, visitado, cluster)
                clusters.append(cluster)

        return clusters

    # Função auxiliar de DFS para marcar os componentes no grafo transposto
    def dfs_cluster(self, v, visitado, cluster):
        visitado[v] = True
        cluster.append(v)
        for vizinho in self.grafo[v]:
            if not visitado[vizinho]:
                self.dfs_cluster(vizinho, visitado, cluster)

    # Função para sugerir amigos baseando-se em amigos em comum
    def sugerir_amigos(self, usuario):
        amigos = set(self.grafo[usuario])
        sugestoes = set()

        for amigo in amigos:
            for potencial in self.grafo[amigo]:
                if potencial != usuario and potencial not in amigos:
                    sugestoes.add(potencial)

        return list(sugestoes)

# Criação do grafo
grafo = Grafo(7)  # Exemplo com 7 nós

# Adicionando arestas (usuários seguem outros usuários)
arestas = [
    (0, 1),  # A segue B
    (1, 2),  # B segue C
    (2, 0),  # C segue A
    (1, 3),  # B segue D
    (3, 4),  # D segue E
    (4, 5),  # E segue F
    (5, 3),  # F segue D
    (6, 4),  # G segue E
    (6, 5)   # G segue F
]

for u, v in arestas:
    grafo.adicionar_aresta(u, v)

# Encontrando componentes fortemente conectados
clusters = grafo.kosaraju()

# Mostrando os clusters
print("Componentes fortemente conectados encontrados:")
for i, cluster in enumerate(clusters):
    print(f"Cluster {i + 1}: {cluster}")

# Sugerindo amigos para o usuário 0 (A)
sugestoes = grafo.sugerir_amigos(0)
print(f"\nSugestões de amigos para o usuário 0: {sugestoes}")

# Visualizando o grafo
G = nx.DiGraph()
G.add_edges_from(arestas)

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
