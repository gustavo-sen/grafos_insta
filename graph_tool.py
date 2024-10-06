import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.cm as cm
from collections import defaultdict



# Inicialização do grafo
def criar_grafo():
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
    grafo_transposto =  criar_grafo()
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


# Função para visualizar as sugestões de amizade para um nó específico
def visualizar_sugestoes_para_no(no, grafo, clusters, pos):
    # Criando um grafo apenas com as sugestões de amizade do nó específico
    G_sugestoes_no = nx.DiGraph()

    sugestoes = sugerir_amigos(grafo, no, clusters)
    for usuario in sugestoes:
        G_sugestoes_no.add_edge(no, usuario)

    # Visualizando o grafo com as sugestões de amizade para o nó específico
    plt.figure(figsize=(6, 5))
    nx.draw(G_sugestoes_no, pos, with_labels=True, node_color="red", edge_color="red", 
            node_size=800, font_size=10, font_color="white", arrows=True)
    plt.title(f"Grafo com Sugestões de Amizade para o Nó {no}")
    plt.show()