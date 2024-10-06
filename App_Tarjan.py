import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict

# Função de DFS que implementa o algoritmo de Tarjan
def strongconnect(current_node, graph, indices, lowlink, stack, cluster_list, index):
    indices[current_node] = index                                 # Atribui o índice atual ao vértice v
    lowlink[current_node] = index                                 # Inicializa lowlink(menor indice) com o índice atual
    index += 1                                                    # Incrementa o índice para o próximo vértice
    stack.append(current_node)                                    # Adiciona vertice atual à pilha

    for neighbor in graph[current_node]:                                                            # Percorre os vizinhos do vértice atual
        if indices[neighbor] == -1:                                                                 # Se o vizinho não foi visitado
            index = strongconnect(neighbor, graph, indices, lowlink, stack, cluster_list, index)    
            lowlink[current_node] = min(lowlink[current_node], lowlink[neighbor])                   # Atualiza lowlink de vertice atual
        elif neighbor in stack:                                                                     # Verifica se o vizinho está na Stack de processamento
            lowlink[current_node] = min(lowlink[current_node], indices[neighbor])                   # Atualiza lowlink de vértice atual

    
    if lowlink[current_node] == indices[current_node]:                 # Se vértice atual é uma raiz de um cluster, ou seja, o menor indice
        cluster = []                                        
        while True:
            removed_node = stack.pop()                                 # Remove o último vértice da pilha
            cluster.append(removed_node)                               # Adiciona w(vértice que está sendo retirado da pilha) ao SCC
            if removed_node == current_node:                           # Se no anterior é igual a no atual, saiu terminou o cluster
                break
        cluster_list.append(cluster)                                   # Adiciona o Cluster à lista de Clusters

    return index 

def tarjan(graph, num_vertices):
    # Lista de indices
    indices = [-1] * num_vertices   
    lowlink = [-1] * num_vertices    

    stack = []                       
    cluster_list = []                        
    index = 0                        

    # Realiza um teste para ver se o vertice ja foi visitado, caso nao, visita.
    for v in range(num_vertices):
        if indices[v] == -1:                                                                    
            index = strongconnect(v, graph, indices, lowlink, stack, cluster_list, index)

    return cluster_list

# Função para sugerir amigos dentro dos componentes
def sugerir_amigos(cluster_list):
    sugestoes = defaultdict(list)                       # Cria um dicionário para armazenar sugestões de amigos

    for cluster in cluster_list:                        # Percorre cada componente fortemente conectado
        for i in range(len(cluster)):                   # Para cada usuário no componente
            for j in range(i + 1, len(cluster)):        # Compara com os outros usuários
                usuario1 = cluster[i]  
                usuario2 = cluster[j]  
                sugestoes[usuario1].append(usuario2)    # Sugere usuário 2 para usuário 1

    return sugestoes 

# ============================================= VISUAL =======================================================#
def desenhar_grafo(graph, sccs):
    G = nx.DiGraph()

    for u in graph:
        for v in graph[u]:
            G.add_edge(u, v)  

    cores = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink', 'gray']
    cor_map = {node: cores[idx % len(cores)] for idx, scc in enumerate(sccs) for node in scc} 

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color=[cor_map.get(no, 'black') for no in G.nodes],
            node_size=800, font_size=10, font_color='white', arrows=True, edge_color='black')

    plt.title("Componentes Fortemente Conectados (Tarjan)")  # Título do gráfico
    plt.show() 

# ========================================== Main =========================================================#
def add_edge(graph, u, v):
    graph[u].append(v) 

def main():
    num_vertices = 5                        # Número de vértices
    graph = defaultdict(list) 

    add_edge(graph, 0, 2)
    add_edge(graph, 2, 1)
    add_edge(graph, 1, 0)
    add_edge(graph, 0, 3)
    add_edge(graph, 3, 4)

    cluster_list = tarjan(graph, num_vertices)
    print("Componentes Fortemente Conectados:", cluster_list)
    print("---------------------")

    # Sugestão de amigos
    sugestoes = sugerir_amigos(cluster_list) 

    print("Sugestões de amigos:")  
    for usuario, amigos in sugestoes.items():  
        print(f"Usuário {usuario} pode seguir: {amigos}") 
    
    desenhar_grafo(graph, cluster_list)

if __name__ == "__main__":
    main()  
