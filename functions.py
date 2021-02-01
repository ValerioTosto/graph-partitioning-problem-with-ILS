import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import random
import statistics
import os
import constant

# Draw Partitions
def draw_graph(G, pos, title = '', instance = ''):
    plt.clf()
    (P1, P2) = get_partitions(G)
    nx.draw_networkx_nodes(G, pos, nodelist=P1, node_color='#de3c19')
    nx.draw_networkx_nodes(G, pos, nodelist=P2)
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edges(G, pos, arrows=False)
    nx.draw_networkx_edges(G, pos, edgelist=generate_cut_edge_list(G), width=3, alpha=0.5, edge_color='r')
    print(title, ' cut-size - ', cut_size_value(G))

    red_patch = mpatches.Patch(color='#de3c19', label='# Partition 1: ' + str(len(P1)))
    blue_patch = mpatches.Patch(color='#1f78b4', label='# Partition 2: ' + str(len(P2)))
    plt.legend(handles=[red_patch, blue_patch])

    if not os.path.exists(constant.RESULTS_PATH + instance + '/' + constant.IMAGE_PATH):
        os.makedirs(constant.RESULTS_PATH + instance + '/' + constant.IMAGE_PATH)
    plt.savefig(constant.RESULTS_PATH + instance + '/' + constant.IMAGE_PATH + '/' + title + ' cut-size - ' + str(cut_size_value(G)) + '.png')

# Generate edge_list from partitions
def generate_cut_edge_list(G):
    (P1, P2) = get_partitions(G)
    edge_list = []
    for i,u in enumerate(P1):
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
def generate_solution(G, seed=int):
    nodes = G.number_of_nodes()
    random.seed(seed)
    indexes = random.sample(range(0, nodes), round(nodes/2))
    for i,node in enumerate(G.nodes()):
        if i in indexes:
            G.nodes[node]['partition'] = 1
        else:
            G.nodes[node]['partition'] = 0
    return G

# Get partitions list from a given graph
def get_partitions(G):
    V1 = []
    V2 = []
    for u in G.nodes():
        if G.nodes[u]['partition'] == 1:
            V1.append(u)
        else:
            V2.append(u)
    return (V1, V2)

# Generate neighborhood from a given graph
def generate_multiple_neighborhood(G):
    (P1, P2) = get_partitions(G)
    Smn = []
    Smn = generate_neighborhood_from_partition(G, P1, Smn)
    Smn = generate_neighborhood_from_partition(G, P2, Smn)
        
    return Smn


# Generate neighborhood from a given graph
def generate_neighborhood_from_partition(G, P, Smn):
    max_ext_neighborhood = 0
    min_int_neighborhood = len(G.edges())
    node = 0 #node with max external neighborhood and min internal neighborhood

    for i,u in enumerate(P):
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

def identify_isolated_nodes(G, P):
    min_int_neighborhood = 9999999999999
    max_ratio = 0
    #node = 0 #node with max external neighborhood and min internal neighborhood
    nodes_indexes_list =[]

    for i,u in enumerate(P):
        ext_neighborhood = 0
        int_neighborhood = 0
        for v in G.neighbors(u):
            if G.nodes[v]['partition'] != G.nodes[u]['partition']:
                ext_neighborhood += 1
            else:
                int_neighborhood += 1
        
        u_neighborhood = len(list(G.neighbors(u)))
        u_ratio = ext_neighborhood/u_neighborhood
        
        if u_ratio > max_ratio:
            nodes_indexes_list.clear()
            nodes_indexes_list.append(i)
            min_int_neighborhood = int_neighborhood
            max_ratio = u_ratio
            #node = u
        elif u_ratio == max_ratio:
            nodes_indexes_list.append(i)
            if int_neighborhood < min_int_neighborhood:
                min_int_neighborhood = int_neighborhood
                #node = u

    return nodes_indexes_list

def switch_isolated_nodes(G):
    (P1, P2) = get_partitions(G)
    ns_G = G.copy()

    nodes_list_1 = identify_isolated_nodes(G, P1)
    nodes_list_2 = identify_isolated_nodes(G, P2)

    nodes_to_swap = min(len(nodes_list_1), len(nodes_list_2))
    for i in range(nodes_to_swap):
        node_1 = P1[nodes_list_1[i]]
        node_2 = P2[nodes_list_2[i]]
        ns_G.nodes[node_1]['partition'], ns_G.nodes[node_2]['partition'] = G.nodes[node_2]['partition'], G.nodes[node_1]['partition']
    
    return ns_G

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
    found_better_solution = False
    i = 0

    # Define stop condition number (0.5% of nodes)
    max_loop = round(0.5 * S0.number_of_nodes()/100)
    while not found_better_solution and i < max_loop :

        # Generate candidate solutions (partial neighborhood) from St
        Smn = generate_multiple_neighborhood(St)
        # Select a solution from Smn to replace the current solution St 
        St = best_neighborhood(Smn)

        # Improving best neighborhood result with:
        # 1. best #ext/#neighbors ratio switch (best P1 with best P2)
        St_s = switch_isolated_nodes(St)
        if cut_size_value(St_s) < cut_size_value(St):
            St = St_s

        if cut_size_value(St) < cut_size_value(best_local_solution):
            best_local_solution = St
        else:
            found_better_solution = True

        i += 1

    return best_local_solution

# Make perturb using swap
def perturbation(G, seed):
    (P1, P2) = get_partitions(G)
    ns_G = G.copy()
    number_swap = round(20 * min(len(P1), len(P2))/100) #swap only 20%

    for x in range(number_swap):
        i = random.randint(0, len(P1)-2)
        if max(len(P1)-len(P2), len(P2)-len(P1)) > 1 :
            print(len(P1), len(P2), i)
        ns_G.nodes[P1[i]]['partition'], ns_G.nodes[P2[i]]['partition'] = G.nodes[P2[i]]['partition'], G.nodes[P1[i]]['partition']

    #print('original: ', cut_size_value(G), ' -> final pert: ', cut_size_value(ns_G))
    return ns_G

# Accept solution
def accept(G1, G2):
    if cut_size_value(G1) < cut_size_value(G2):
        return G1
    return G2

#Calculate the follow performance indexes:
# - best solution: migliore soluzione trovata tra le 10 runs;
# - mean solutions: media delle migliori soluzioni trovate nei 10 runs;
# - standard deviation (sulla means di cui sopra).
def calculate_performance(cut_size_list, instance):
    if not os.path.exists(constant.RESULTS_PATH + instance + '/'):
        os.makedirs(constant.RESULTS_PATH + instance + '/')
    f = open(constant.RESULTS_PATH + instance + '/performance.txt', 'w')
    f.write('best solution: ' + str(min(cut_size_list)) + '\n')
    f.write('mean solutions: ' + str(statistics.mean(cut_size_list)) + '\n')
    f.write('standard deviation: ' + str(statistics.stdev(cut_size_list)) + '\n')
    f.close()