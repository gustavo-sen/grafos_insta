import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.cm as cm
from collections import defaultdict, deque

# Função para criar o grafo
def criar_grafo():
    return defaultdict(list)

# Função para adicionar arestas ao grafo
def adicionar_aresta(grafo, u, v):
    grafo[u].append(v)
    if v not in grafo:
        grafo[v].append(None)

# ==================================== ALGORITMO ======================================================

# Função de DFS para o passo 1 
def dfs(graph, v, visited, stack):
    visited[v] = True                                       # O nó atual agora foi visitado
    for neighbor in graph[v]:                               # Busca os vizinhos de nó atual
        if (neighbor != None) and (not visited[neighbor]):  # Se o vizinho não foi visitado chama o DFS
            dfs(graph, neighbor, visited, stack)                                   
    stack.append(v)                                          # Adiciona na pilha

# Função de DFS para o passo 2
def dfs_transposto(graph, v, visited, scc_stack):
    visited[v] = True                                       # O nó atual agora foi visitado
    scc_stack.append(v)                                     # Adiciona o nó na lista do cluster
    for u in graph:                                         # Para cada nó no Grafo   
        if v in graph[u] and not visited[u]:                # Se o nó atual está conectado ao nó u e não foi visitado
            dfs_transposto(graph, u, visited, scc_stack)    # Cham o DFS, Se não vai retornar o cluster



def kosaraju(grafo, num_vertices):
    # Passo 1: Preencher a pilha
    stack = []                              # Cria a pilha
    visited = [False] * num_vertices        # Cria lista para armazenar os nós visitados
    for i in range(num_vertices):           # Percorre os nós do grafo
        if not visited[i]:                  # Se não foi visitado chama o DFS
            dfs(grafo, i, visited, stack)

    # Passo 2: Fazer a DFS na ordem inversa usando a pilha
    visited = [False] * num_vertices        # Limpa a lista para armazenar os nós visitados
    sccs = []                               # Cria a lista para armazenar os clusters
    while stack:                            # Enquanto a pilha não estiver vazia
        v = stack.pop()                     # Armazena o ultimo nó da pilha na variavel v
        if not visited[v]:                  # Se o nó v não foi visitado
            scc_stack = []                  # Cria lista para armazenar novo cluster
            dfs_transposto(grafo, v, visited, scc_stack)        # Chama o DFS para a pilha
            sccs.append(scc_stack)          # Adicionao cluster a uma lista com todos os clusters

    return sccs


# Função para sugerir amigos dentro dos clusters
def sugerir_amigos(grafo, clusters):
    sugestoes = defaultdict(list)                   # Cria um dicionario(grafo) para as sugestões de amizade

    for cluster in clusters:                        # Para cada cluster entre todos os clusters
        for i in range(len(cluster)):               # Para cada nó(i) dentro do cluster
            for j in range(i + 1, len(cluster)):    # Para cada nó(j) sucessor do nó(i)
                usuario1 = cluster[i]
                usuario2 = cluster[j]
                # Verifica se não há conexão direta entre os usuários
                if usuario2 not in grafo[usuario1]:         # Se o nó(j) não segue ao nó(i)
                    sugestoes[usuario1].append(usuario2)    # Sugeri para seguir
                if usuario1 not in grafo[usuario2]:         # Se o nó(i) não segue ao nó(j)
                    sugestoes[usuario2].append(usuario1)    # Sugeri para seguir

    return sugestoes                                        # Retorna todas as sugestões  


# ==================================== VISUAL ======================================================

# Função para desenhar o grafo e seus clusters fortemente conectados
def desenhar_grafo(grafo, clusters):
    G = nx.DiGraph()  # Grafo direcionado

    # Adiciona arestas ao grafo
    for origem, destinos in grafo.items():
        for destino in destinos:
            if destino != None:
                G.add_edge(origem, destino)

    # Atribui cores aos nós de acordo com o cluster fortemente conectado
    cor_map = {}
    cores = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink', 'gray']
    for idx, cluster in enumerate(clusters):
        cor = cores[idx % len(cores)]
        for no in cluster:
            cor_map[no] = cor

    # Desenha o grafo com cores para cada cluster
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color=[cor_map.get(no, 'black') for no in G.nodes], 
            node_size=800, font_size=10, font_color='white', arrows=True, edge_color='black')

    plt.title("clusters Fortemente Conectados")
    plt.show()



# Função para desenhar o grafo apenas com as sugestões de amizade
def desenhar_grafo_sugestoes(grafo, sugestoes):
    G = nx.DiGraph()  # Grafo direcionado

    # Adiciona nós ao grafo
    for origem in grafo:
        G.add_node(origem)

    # Adiciona arestas sugeridas ao grafo
    for usuario, amigos in sugestoes.items():
        for amigo in amigos:
            G.add_edge(usuario, amigo, color='gray', style='dashed')

    # Desenha o grafo apenas com as sugestões
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue',
            node_size=800, font_size=10, font_color='black', arrows=True, edge_color='gray', style='dashed')

    plt.title("Sugestões de Amizade")
    plt.show()

# ======================================== Main ======================================================
if __name__ == "__main__":
    
    grafo = criar_grafo()
    adicionar_aresta(grafo, 0, 2)
    adicionar_aresta(grafo, 2, 1)
    adicionar_aresta(grafo, 1, 0)
    adicionar_aresta(grafo, 0, 3)
    adicionar_aresta(grafo, 3, 4)
    adicionar_aresta(grafo, 5, 4)
    adicionar_aresta(grafo, 6, 5)
    adicionar_aresta(grafo, 5, 6)

    num_vertices = len(grafo.keys())
    

    clusters = kosaraju(grafo, num_vertices)
    print("clusters fortemente conectados:", clusters)

    desenhar_grafo(grafo, clusters)

    # Sugestão de amigos
    sugestoes = sugerir_amigos(grafo, clusters)
    print("Sugestões de amigos:")
    for usuario, amigos in sugestoes.items():
        print(f"Usuário {usuario} pode seguir: {amigos}")

    desenhar_grafo_sugestoes(grafo, sugestoes)