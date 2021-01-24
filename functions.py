import networkx as nx
import matplotlib.pyplot as plt
import random

# Draw Partitions
def draw_graph(G, pos, title = ''):
    (P1, P2) = get_partitions(G)
    #(P1, P2) = (v1, v2)
    nx.draw_networkx_nodes(G, pos, nodelist=P1, node_color='#de3c19')
    nx.draw_networkx_nodes(G, pos, nodelist=P2)
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edges(G, pos, arrows=False)
    nx.draw_networkx_edges(G, pos, edgelist=generate_cut_edge_list(G), width=3, alpha=0.5, edge_color='r')
    print(title, ' cut-size - ', cut_size_value(G))
    plt.title(title + ' cut-size - ' + str(cut_size_value(G)))
    plt.show()

# Generate edge_list from partitions
def generate_cut_edge_list(G):
    edge_list = []
    for u in G.nodes():
        for v in G.neighbors(u):
            if G.nodes[v]['partition'] != G.nodes[u]['partition']:
                edge_list.extend([(u,v)])
    return edge_list

# Calculate Partitions Cut Size
def cut_size_value_old(G, P1, P2):
    cut_size = 0
    for x in P1:
        for y in P2:
            if G.has_edge(x, y) or G.has_edge(y, x):
                cut_size += 1
    return cut_size

# Calculate Partitions Cut Size
def cut_size_value(G):
    return len(generate_cut_edge_list(G))

# Print Graph info
def graph_info(K, n, G, P1, P2):
    print('K - ', K)
    print('# cycle - ', n)
    print('Graph nodes - ', G.number_of_nodes())
    print('Graph edges - ', len(G.edges()))
    print('# Partition 1 - ', len(P1))
    print('# Partition 2 - ', len(P2))

# Generate random partitions
def generate_solution(G):
    nodes = G.number_of_nodes()
    nodes_list = list(G.nodes)
    #V1 = []
    #V2 = []
    indexes = random.sample(range(0, nodes), round(nodes/2))
    for i in indexes:
        #V1.append(nodes_list[i])
        G.nodes[nodes_list[i]]['partition'] = 1
    #V2.extend(set(nodes_list) - set(V1))

    return get_partitions(G)


# Generate random partitions
def get_partitions(G):
    nodes_list = list(G.nodes)
    V1 = []
    V2 = []
    for u in nodes_list:
        if G.nodes[u]['partition'] == 1:
            V1.append(u)
        else:
            V2.append(u)

    return (V1, V2)

# Generate neighborhood
def generate_neighborhood(G, S):
    V1, V2 = S[0].copy(), S[1].copy()

    nodes = G.number_of_nodes()
    nodes_list = list(G.nodes)

    max_neighbors_v1 = 0
    max_neighbors_v1_index = 0
    max_neighbors_v2 = 0
    max_neighbors_v2_index = 0

    for i,x in enumerate(V1):
        count = 0
        for y in G.neighbors(x):
            if y in V2:
                count += 1
        if count > max_neighbors_v1:
            max_neighbors_v1 = count
            max_neighbors_v1_index = i

    for i,x in enumerate(V2):
        count = 0
        for y in G.neighbors(x):
            if y in V1:
                count += 1
        if count > max_neighbors_v2:
            max_neighbors_v2 = count
            max_neighbors_v2_index = i
    
    V2.append(V1.pop(max_neighbors_v1_index))
    V1.append(V2.pop(max_neighbors_v2_index))

    Sn = [V1, V2]
    return Sn

def generate_neighborhood2(G, S):
    V1, V2 = S[0].copy(), S[1].copy()

    nodes = G.number_of_nodes()
    nodes_list = list(G.nodes)

    min_neighbors_v1 = nodes
    min_neighbors_v1_index = 0
    min_neighbors_v2 = nodes
    min_neighbors_v2_index = 0

    for i,x in enumerate(V1):
        count = 0
        for y in G.neighbors(x):
            if y in V2:
                count += 1
        if count < min_neighbors_v1:
            min_neighbors_v1 = count
            min_neighbors_v1_index = i

    for i,x in enumerate(V2):
        count = 0
        for y in G.neighbors(x):
            if y in V1:
                count += 1
        if count < min_neighbors_v2:
            min_neighbors_v2 = count
            min_neighbors_v2_index = i
    
    V2.append(V1.pop(min_neighbors_v1_index))
    V1.append(V2.pop(min_neighbors_v2_index))

    Sn = [V1, V2]
    return Sn

def generate_multiple_neighborhood(G, S):
    V1, V2 = S[0].copy(), S[1].copy()
    Smn = []
    nodes = G.number_of_nodes()
    nodes_list = list(G.nodes)

    max_cycle = len(V1)
    if len(V1) != len(V2):
        max_cycle = min(len(V1), len(V2))
    
    for i in range(max_cycle):
        V2.append(V1.pop(i))
        V1.append(V2.pop(i))
        Sn = [V1.copy(), V2.copy()]
        Smn.append(Sn)
    
    return Smn

def generate_multiple_neighborhood2(G, S):
    V1, V2 = S[0].copy(), S[1].copy()
    Smn = []
    nodes = G.number_of_nodes()
    nodes_list = list(G.nodes)

    max_ext_neighborhood_v1 = 0
    max_int_neighborhood_v1 = len(G.edges())
    max_neighborhood_v1_index = 0
    max_ext_neighborhood_v2 = 0
    max_int_neighborhood_v2 = len(G.edges())
    max_neighborhood_v2_index = 0

    for i,x in enumerate(V1):
        ext_neighborhood = 0
        int_neighborhood = 0
        for j,y in enumerate(G.neighbors(x)):
            if y in V2:
                ext_neighborhood += 1
            else:
                int_neighborhood += 1

        if ext_neighborhood > max_ext_neighborhood_v1 and int_neighborhood < max_int_neighborhood_v1:
            max_ext_neighborhood_v1 = ext_neighborhood
            max_int_neighborhood_v1 = int_neighborhood
            max_neighborhood_v1_index = i

    for i,x in enumerate(V2):
        ext_neighborhood = 0
        int_neighborhood = 0
        for j,y in enumerate(G.neighbors(x)):
            if y in V1:
                ext_neighborhood += 1
            else:
                int_neighborhood += 1

        if ext_neighborhood > max_ext_neighborhood_v2 and int_neighborhood < max_int_neighborhood_v2:
            max_ext_neighborhood_v2 = ext_neighborhood
            max_ext_neighborhood_v2 = int_neighborhood
            max_neighborhood_v2_index = i
    
    V2.append(V1.pop(max_neighborhood_v1_index))
    V1.append(V2.pop(max_neighborhood_v2_index))
    Sn = [V1.copy(), V2.copy()]
    Smn.append(Sn)
    
    return Smn

def generate_multiple_neighborhood_graph(G):
    Smn = []

    max_ext_neighborhood = 0
    min_int_neighborhood = len(G.edges())
    node = 0 #node with max external neighborhood and min internal neighborhood

    for u in G.nodes():
        ext_neighborhood = 0
        int_neighborhood = 0
        for v in G.neighbors(u):
            if G.nodes[v]['partition'] != G.nodes[u]['partition']:
                ext_neighborhood += 1
            else:
                int_neighborhood += 1

            if ext_neighborhood > max_ext_neighborhood:
                    max_ext_neighborhood = ext_neighborhood
                    min_int_neighborhood = int_neighborhood
                    node = v
            elif ext_neighborhood == max_ext_neighborhood:
                if int_neighborhood < min_int_neighborhood:
                    min_int_neighborhood = int_neighborhood
                    node = v
    
    for v in G.neighbors(node):
        #print(node, ' - ', v, ' - ', len(list(G.neighbors(node))))
        if G.nodes[node]['partition'] != G.nodes[v]['partition']:
            ns_G = G.copy()
            ns_G.nodes[node]['partition'], ns_G.nodes[v]['partition'] = G.nodes[v]['partition'], G.nodes[node]['partition']
            #print (node, ' - ', G.nodes[node]['partition'], '->', ns_G.nodes[node]['partition'])
            #print('cutsize=', cut_size_value(ns_G))
            Smn.append(ns_G.copy())
        
    return Smn

def best_neighborhood_old(G, Smn):
    index = 0
    bcsv = len(G.edges())
    for i,Sn in enumerate(Smn):
        csv = cut_size_value(G, Sn[0], Sn[1])
        if csv < bcsv:
            bcsv = csv
            index = i
    
    return Smn[index]


def best_neighborhood(Smn):
    index = 0
    bcsv = len(Smn[0].edges())
    #bcsv=99999999999999999
    for i,Sn in enumerate(Smn):
        csv = cut_size_value(Sn)
        if csv < bcsv:
            bcsv = csv
            index = i
    #print('bestcutsize=', cut_size_value(Smn[index]))
    return Smn[index]

# Make perturb using swap
def swap_old(P1, P2):
    for x in range(round(len(P1)/5)): #swap only 5%
        i = random.randint(0, len(P1)-1)
        P1[i], P2[i] = P2[i], P1[i]

def swap(G, P1, P2):
    ns_G = G.copy()
    for x in range(round(len(P1)/5)): #swap only 5%
        i = random.randint(0, len(P1)-1)
        #P1[i], P2[i] = P2[i], P1[i]
        ns_G.nodes[P1[i]]['partition'], ns_G.nodes[P2[i]]['partition'] = G.nodes[P2[i]]['partition'], G.nodes[P1[i]]['partition']
    return ns_G

def local_search(G, S):
    V1, V2 = S[0].copy(), S[1].copy()
    # do something