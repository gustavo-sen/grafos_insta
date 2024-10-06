import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.cm as cm
from collections import defaultdict

#Criacao grafo
def criar_grafo():
    return {'adj': defaultdict(list), 'rev_adj': defaultdict(list)}

def adicionar_aresta(grafo, origem, destino):
    grafo['adj'][origem].append(destino)
    grafo['rev_adj'][destino].append(origem)


#==========================Kosaraju====================================#

# Função de DFS para o passo 1 (usando as arestas diretas)
def dfs_1(grafo, v, visitado, pilha):
    visitado[v] = True
    for vizinho in grafo['adj'][v]:
        if not visitado[vizinho]:
            dfs_1(grafo, vizinho, visitado, pilha)
    pilha.append(v)

# Função de DFS para o passo 3 (usando as arestas reversas)
def dfs_2(grafo, v, visitado, componente):
    visitado[v] = True
    componente.append(v)
    for vizinho in grafo['rev_adj'][v]:
        if not visitado[vizinho]:
            dfs_2(grafo, vizinho, visitado, componente)

# Função principal para encontrar componentes fortemente conectados
def kosaraju(grafo):
    vertices = list(set(grafo['adj'].keys()).union(set(grafo['rev_adj'].keys()))) # conta a quantidade de itens

    # Passo 1: Realizar DFS para preencher a pilha
    pilha = []
    visitado = {v: False for v in vertices}
    for v in vertices:
        if not visitado[v]:
            dfs_1(grafo, v, visitado, pilha)

    # Passo 2: Realizar DFS no grafo transposto na ordem dada pela pilha
    visitado = {v: False for v in vertices}
    clusters = []
    while pilha:
        v = pilha.pop()
        if not visitado[v]:
            componente = []
            dfs_2(grafo, v, visitado, componente)
            clusters.append(componente)

    return clusters

# Função para desenhar o grafo e seus componentes fortemente conectados
def desenhar_grafo(grafo, componentes):
    G = nx.DiGraph()  # Grafo direcionado

    # Adiciona arestas ao grafo
    for origem, destinos in grafo['adj'].items():
        for destino in destinos:
            G.add_edge(origem, destino)

    # Atribui cores aos nós de acordo com o componente fortemente conectado
    cor_map = {}
    cores = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink', 'gray']
    for idx, componente in enumerate(componentes):
        cor = cores[idx % len(cores)]
        for no in componente:
            cor_map[no] = cor

    # Desenha o grafo com cores para cada componente
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color=[cor_map.get(no, 'black') for no in G.nodes], 
            node_size=800, font_size=10, font_color='white', arrows=True, edge_color='black')

    plt.title("Componentes Fortemente Conectados")
    plt.show()


# Função para sugerir amigos dentro dos componentes
def sugerir_amigos(grafo, componentes):
    sugestoes = defaultdict(list)

    for componente in componentes:
        for i in range(len(componente)):
            for j in range(i + 1, len(componente)):
                usuario1 = componente[i]
                usuario2 = componente[j]
                # Verifica se não há conexão direta entre os usuários
                if usuario2 not in grafo['adj'][usuario1]:
                    sugestoes[usuario1].append(usuario2)
                if usuario1 not in grafo['adj'][usuario2]:
                    sugestoes[usuario2].append(usuario1)

    return sugestoes

# Função para desenhar o grafo apenas com as sugestões de amizade
def desenhar_grafo_sugestoes(grafo, sugestoes):
    G = nx.DiGraph()  # Grafo direcionado

    # Adiciona nós ao grafo
    for origem in grafo['adj']:
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

# Exemplo de uso
if __name__ == "__main__":
    
    grafo = criar_grafo()
    adicionar_aresta(grafo, 0, 2)
    adicionar_aresta(grafo, 2, 1)
    adicionar_aresta(grafo, 1, 0)
    adicionar_aresta(grafo, 0, 3)
    adicionar_aresta(grafo, 3, 4)

    clusters = kosaraju(grafo)
    print("Componentes fortemente conectados:", clusters)

    desenhar_grafo(grafo, clusters)

    # Sugestão de amigos
    sugestoes = sugerir_amigos(grafo, clusters)
    print("Sugestões de amigos:")
    for usuario, amigos in sugestoes.items():
        print(f"Usuário {usuario} pode seguir: {amigos}")

    desenhar_grafo_sugestoes(grafo, sugestoes)
