import networkx as nx
import matplotlib.pyplot as plt
import random

# Draw Partitions
def draw_graph(G, pos, title = ''):
    (P1, P2) = get_partitions(G)
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

# Calculate graph cut-size
def cut_size_value(G):
    return len(generate_cut_edge_list(G))

# Print problem info
def problem_info(K, n, G):
    (P1, P2) = get_partitions(G)
    print('K - ', K)
    print('# cycle - ', n)
    print('Graph nodes - ', G.number_of_nodes())
    print('Graph edges - ', len(G.edges()))
    print('# Partition 1 - ', len(P1))
    print('# Partition 2 - ', len(P2))

# Generate random partitions from a given graph
def generate_solution(G):
    nodes = G.number_of_nodes()
    nodes_list = list(G.nodes)
    indexes = random.sample(range(0, nodes), round(nodes/2))
    for i in indexes:
        G.nodes[nodes_list[i]]['partition'] = 1
    return G

# Get partitions list from a given graph
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

# Generate neighborhood from a given graph
def generate_multiple_neighborhood(G):
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
                    node = u
            elif ext_neighborhood == max_ext_neighborhood:
                if int_neighborhood < min_int_neighborhood:
                    min_int_neighborhood = int_neighborhood
                    node = u
    
    for v in G.neighbors(node):
        if G.nodes[node]['partition'] != G.nodes[v]['partition']:
            ns_G = G.copy()
            ns_G.nodes[node]['partition'], ns_G.nodes[v]['partition'] = G.nodes[v]['partition'], G.nodes[node]['partition']
            Smn.append(ns_G.copy())
        
    return Smn

def best_neighborhood(Smn):
    index = 0
    bcsv = len(Smn[0].edges())
    for i,Sn in enumerate(Smn):
        csv = cut_size_value(Sn)
        if csv < bcsv:
            bcsv = csv
            index = i
    return Smn[index]

def local_search(S0):
    best_local_solution = S0
    St = S0
    while True:
        # Generate candidate solutions (partial neighborhood) from St
        Smn = generate_multiple_neighborhood(St)
        # Select a solution from Smn to replace the current solution St 
        St = best_neighborhood(Smn)
        
        #print('best_local_solution: ', cut_size_value(best_local_solution), ' -> new: ', cut_size_value(St))

        if cut_size_value(St) < cut_size_value(best_local_solution):
            best_local_solution = St
        else:
            break

    return best_local_solution

# Make perturb using swap
def perturbation(G):
    (P1, P2) = get_partitions(G)
    ns_G = G.copy()
    for x in range(round(len(P1)/5)): #swap only 5%
        i = random.randint(0, len(P1)-1)
        ns_G.nodes[P1[i]]['partition'], ns_G.nodes[P2[i]]['partition'] = G.nodes[P2[i]]['partition'], G.nodes[P1[i]]['partition']
    #print('original: ', cut_size_value(G), ' -> final pert: ', cut_size_value(ns_G))
    return ns_G

# Accept solution
def accept(G1, G2):
    #print('G1: ', cut_size_value(G1), ' -> G2: ', cut_size_value(G2))
    if cut_size_value(G1) < cut_size_value(G2):
        return G1
    return G2
