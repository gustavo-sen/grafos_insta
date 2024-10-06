import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.cm as cm
from collections import defaultdict

# Inicialização do grafo
def criar_grafo(vertices):
    return defaultdict(list)

# Função para adicionar arestas ao grafo
def adicionar_aresta(grafo, u, v):
    grafo[u].append(v)

def dfs(grafo, v, visitado, pilha):

    visitado[v] = True
    for vizinho in grafo[v]:
        if not visitado[vizinho]:
            dfs(grafo, vizinho, visitado, pilha)
    pilha.append(v)


# Função para transpor o grafo
def transpor(grafo):
    grafo_transposto =  criar_grafo(len(grafo))
    for i in grafo:
        for j in grafo[i]:
            adicionar_aresta(grafo_transposto, j, i)
    return grafo_transposto


# Função principal para encontrar componentes fortemente conectados
def kosaraju(grafo):

    # Passo 1: Realizar DFS para preencher a pilha  
    pilha = []
    visitado = [False] * len(grafo)
    for i in range(len(grafo)):
        if not visitado[i]:
            dfs(grafo, i, visitado, pilha)

    # Passo 2: Transpor o grafo
    grafo_transposto = transpor(grafo)


    # Passo 3: Realizar DFS no grafo transposto na ordem dada pela pilha
    visitado = [False] * len(grafo)
    clusters = []
    for i in range(len(grafo)):
        if not visitado[i]:
            cluster = []
            dfs(grafo_transposto, i, visitado, cluster)
            clusters.append(cluster)

    return clusters


# Função para sugerir amigos baseando-se em amigos em comum
def sugerir_amigos(grafo, usuario, clusters):
     # Encontrar o cluster ao qual o usuário pertence
    for cluster in clusters:
        if usuario in cluster:
            # Sugerir amigos dentro do cluster que ainda não têm conexão direta com o usuário
            amigos = set(grafo[usuario])
            sugestoes = [v for v in cluster if v != usuario and v not in amigos]
            return sugestoes
    return []


# Criação do grafo usando dicionário
grafo = criar_grafo(7)

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

# Função para visualizar as sugestões de amizade para um nó específico
def visualizar_sugestoes_para_no(no):
    # Criando um grafo apenas com as sugestões de amizade do nó específico
    G_sugestoes_no = nx.DiGraph()

    sugestoes = sugerir_amigos(grafo, no, clusters)
    for usuario in sugestoes:
        G_sugestoes_no.add_edge(no, usuario)

    # Visualizando o grafo com as sugestões de amizade para o nó específico
    plt.figure(figsize=(10, 7))
    nx.draw(G_sugestoes_no, pos, with_labels=True, node_color="red", edge_color="red", 
            node_size=800, font_size=10, font_color="white", arrows=True)
    plt.title(f"Grafo com Sugestões de Amizade para o Nó {no}")
    plt.show()

visualizar_sugestoes_para_no(0)