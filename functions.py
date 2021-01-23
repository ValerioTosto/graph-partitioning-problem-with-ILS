import networkx as nx
import matplotlib.pyplot as plt
import random

# Draw Partitions
def draw_graph(G, pos, P1, P2, title = ''):
    nx.draw_networkx_nodes(G, pos, nodelist=P1, node_color='#de3c19')
    nx.draw_networkx_nodes(G, pos, nodelist=P2)
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edges(G, pos, arrows=False)
    nx.draw_networkx_edges(G, pos, edgelist=generate_edge_list(G, P1, P2), width=3, alpha=0.5, edge_color='r')
    plt.title(title + ' cut-size - ' + str(cut_size_value(G, P1, P2)))
    plt.show()

# Generate edge_list from partitions
def generate_edge_list(G, P1, P2):
    edge_list = []
    for x in P1:
        for y in P2:
            if G.has_edge(x, y) or G.has_edge(y, x):
                edge_list.extend([(x,y)])
    return edge_list

# Calculate Partitions Cut Size
def cut_size_value(G, P1, P2):
    cut_size = 0
    for x in P1:
        for y in P2:
            if G.has_edge(x, y) or G.has_edge(y, x):
                cut_size += 1
    return cut_size

# Print Graph info
def graph_info(K, n, G, P1, P2):
    print('K - ' + str(K))
    print('# cycle - ' + str(n))
    print('Graph nodes - ' + str(len(G.nodes())))
    print('Graph edges - ' + str(len(G.edges())))
    print('# Partition 1 - ' + str(len(P1)))
    print('# Partition 2 - ' + str(len(P2)))

# Generate random partitions
def generate_solution(G):
    nodes = len(G.nodes())
    nodes_list = list(G.nodes)
    V1 = []
    V2 = []
    indexes = random.sample(range(0, nodes), round(nodes/2))
    for i in indexes:
        V1.append(nodes_list[i])
    V2.extend(set(nodes_list) - set(V1))

    return (V1, V2)


# Make perturb using swap
def swap(P1, P2):
    i = random.randint(0, len(P1)-1)
    P1[i], P2[i] = P2[i], P1[i]