# Import libraries
import networkx as nx
import matplotlib.pyplot as plt
import random
import functions as fun
import constant


# Set up graph structure
G = nx.Graph()

instance = constant.TEST_INSTANCE
with open(constant.INSTANCES_PATH + instance, 'r') as in_file:
    lines = in_file.readlines()
    for node,line in enumerate(lines):
        node = int(node)
        if node != 0 and node < len(lines)-1:
            neighborhood = line.replace("\n", "").split(' ')[1:]
            #print(node, neighborhood)
            G.add_node(node, partition = 0)
            for i in neighborhood:
                G.add_edge(node, int(i))

# Draw initial graph
pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'))
nx.draw_networkx_labels(G, pos)
nx.draw_networkx_edges(G, pos, arrows=False)
plt.show()

# Define K set
K = 2

# Define MaxGen number
max_gen = 100

# Define Run value
run = 10

# Define stop condition number
n = 1

# Generate seeds array
# seeds = []
# for i in range(run):
#     seeds.append(random.randint(2233,9999))
# print (seeds)
# seeds = [5483, 8373]
seeds = [4935, 5539, 4827, 6719, 2357, 6385, 6234, 2913, 7284, 8625]

# List of best solution cut-size calculated in each run
cut_size_list = []

for i in range(run):
    # Generate seed
    seed = seeds[i]

    # Define random solution S0
    S_0 = fun.generate_solution(G.copy(), seed)

    # Print problem info
    #fun.problem_info(K, n, S_0)

    # Draw Original Partitions
    fun.draw_graph(S_0, pos, str(i) + ' - Original Partitions', instance)

    # Needed for python warning
    S_star = S_0

    for j in range(max_gen):
        if ( ((j+1)/max_gen * 100) % 10 == 0):
            print('loop percentage: ', int((j+1)/max_gen * 100), ' %', end='\r')
        # Apply a given local search algorithm
        S_star = fun.local_search(S_0)

        # Draw Final LS Partitions
        #fun.draw_graph(S_star, pos, 'Final LS Partitions')

        for x in range(n):

            # Perturb the obtained local optima
            S_first = fun.perturbation(S_star, seed)
            # Apply local search on the perturbed solution #
            S_first_star = fun.local_search(S_first)
            # Accepting criteria
            S_star = fun.accept(S_star, S_first_star)

    # Draw Final ILS Partitions
    fun.draw_graph(S_star, pos, str(i) + ' - Final ILS Partitions', instance)

    cut_size_list.append(fun.cut_size_value(S_star))
    # S_star2 = fun.switch_isolated_nodes(S_star)
    # print('cut-size - ', fun.cut_size_value(S_star), fun.cut_size_value(S_star2))

fun.calculate_performance(cut_size_list, instance)
