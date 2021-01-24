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
n = 3000
    
# Define random solution S0
S_0 = fun.generate_solution(G)

# Print initial graph info
fun.graph_info(K, n, S_0)

# Draw Original Partitions
fun.draw_graph(S_0, pos, 'Original Partitions')

# Apply a given local search algorithm
S_star = fun.local_search(S_0)

# Draw Final LS Partitions
fun.draw_graph(S_star, pos, 'Final LS Partitions')

for x in range(n):
    if ( (x/n * 100) % 10 == 0):
        print('loop percentage: ' + str(x/n * 100) + ' %')

    # Perturb the obtained local optima
    S_first = fun.perturbation(S_star)
    # Apply local search on the perturbed solution #
    S_first_star = fun.local_search(S_first)
    # Accepting criteria
    S_star = fun.accept(S_star, S_first_star)

# Draw Final ILS Partitions
fun.draw_graph(S_star, pos, 'Final ILS Partitions')
