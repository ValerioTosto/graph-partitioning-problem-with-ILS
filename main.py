# Import libraries
import networkx as nx
import matplotlib.pyplot as plt
import random
import functions as fun


# Set up graph structure
G = nx.Graph()

file = open("edges.txt", "r")
for row in file:
    x = row.replace("\n", "").split(" ")
    G.add_node(int(x[0]), partition = 0)
    G.add_node(int(x[1]), partition = 0)
    G.add_edge(int(x[0]), int(x[1]))

# Draw initial graph
pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'))
nx.draw_networkx_labels(G, pos)
nx.draw_networkx_edges(G, pos, arrows=False)
plt.show()

# Define K set
K = 2

# Define cycling number
n = 5000
    
# Define initial solution S
(V1, V2) = fun.generate_solution(G)
S = [V1, V2]

# Print initial graph info
fun.graph_info(K, n, G, V1, V2)

s_cut_size = fun.cut_size_value(G)
#s_cut_size = fun.cut_size_value(G, V1, V2)
#print("cut size: " + str(s_cut_size))


# Draw Original Partitions
fun.draw_graph(G, pos, 'Original Partitions')
    

or_V1 = V1.copy()
or_V2 = V2.copy()

print("V1 - Before editing", V1)
print("V2 - Before editing", V2)

#Sn = fun.generate_neighborhood(G, S)
#
#print("V1 - After editing", V1)
#print("V2 - After editing", V2)
#print("Sn[0] - After editing", Sn[0])
#print("Sn[1] - After editing", Sn[1])
Sn = G
for x in range(n):
    if ( (x/n * 100) % 10 == 0):
        print('loop percentage: ' + str(x/n * 100) + ' %')

    r_V1 = V1.copy()
    r_V2 = V2.copy()

    #print("pre neigh - " + str(fun.cut_size_value(Sn)))
    #Sn = fun.generate_neighborhood(G, [r_V1, r_V2])
    
    Smn = fun.generate_multiple_neighborhood_graph(Sn)
    #Smn = fun.generate_multiple_neighborhood2(G, [r_V1, r_V2])
    #print(len(Smn))
    #Sn = fun.best_neighborhood(G, Smn)
    Sn = fun.best_neighborhood(Smn)

    r_V1, r_V2 = fun.get_partitions(Sn)
    #r_V1 = Sn[0].copy()
    #r_V2 = Sn[1].copy()
    #print("post neigh - " + str(fun.cut_size_value(Sn)))

    #fun.swap(r_V1, r_V2)
    Sn = fun.swap(Sn, r_V1, r_V2)
    r_s_cut_size = fun.cut_size_value(Sn)
    #r_s_cut_size = fun.cut_size_value(G, r_V1, r_V2)
    #print("post swap - " + str(fun.cut_size_value(Sn)))
    #fun.draw_graph(G, pos, r_V1, r_V2, 'temp partitions')
    
    if r_s_cut_size < s_cut_size:
        V1 = r_V1.copy()
        V2 = r_V2.copy()
        s_cut_size = r_s_cut_size
    

print("V1 - After editing", V1)
print("V2 - After editing", V2)
#print("Sn[0] - After editing", Sn[0])
#print("Sn[1] - After editing", Sn[1])

# Draw Final Partition Graph
fun.draw_graph(Sn, pos, 'Final Partitions')