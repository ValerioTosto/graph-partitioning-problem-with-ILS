# Import libraries
import networkx as nx
import matplotlib.pyplot as plt
import random
import functions as fun
#import metis


# Set up graph structure
G = nx.Graph()

file = open("edges.txt", "r")
for row in file:
    x = row.replace("\n", "").split(" ")
    G.add_edges_from([(x[0], x[1])])

# Draw initial graph
pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'))
nx.draw_networkx_labels(G, pos)
nx.draw_networkx_edges(G, pos, arrows=False)
plt.show()

# Define K set
K = 2

# Define cycling number
n = 50000
    
# Define initial solution S
def generate_solution(G):
    nodes = len(G.nodes())
    nodes_list = list(G.nodes)
    #print(nodes_list)
    indexes = random.sample(range(0, nodes), round(nodes/2))
    for i in indexes:
        V1.append(nodes_list[i])
    #print(V1)
    V2.extend(set(nodes_list) - set(V1))
    #print(V2)

    
V1 = []
V2 = []

generate_solution(G)
fun.graph_info(K, n, G, V1, V2)


S = [V1, V2]

s_cut_size = fun.cut_size_value(G, V1, V2)
#print("cut size: " + str(s_cut_size))


# Draw Original Partitions
fun.draw_graph(G, pos, V1, V2, 'Original Partitions')
    

or_V1 = V1.copy()
or_V2 = V2.copy()

# Make mutation using swap
def swap():
    i = random.randint(0, len(r_V1)-1)
    r_V1[i], r_V2[i] = r_V2[i], r_V1[i]

for x in range(n):
    if (x % 5000 == 0):
        print(x)
    r_V1 = V1.copy()
    r_V2 = V2.copy()
    
    swap()
    r_s_cut_size = fun.cut_size_value(G, r_V1, r_V2)
    #fun.draw_graph(G, pos, r_V1, r_V2, 'temp partitions')
    
    if r_s_cut_size < s_cut_size:
        V1 = r_V1.copy()
        V2 = r_V2.copy()
        s_cut_size = r_s_cut_size
    

# Draw Final Partition Graph
fun.draw_graph(G, pos, V1, V2, 'Final Partitions')