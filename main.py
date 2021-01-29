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
            G.add_node(node, partition = 0)
            for i in neighborhood:
                G.add_edge(node, int(i))

# Draw initial graph
pos = nx.spring_layout(G, seed=2233)

# Define K set
K = 2

# Define MaxGen number
max_gen = 1000

# Define Run value
run = 10

# Generate seeds array
# seeds = []
# for i in range(run):
#     seeds.append(random.randint(2233,9999))
# print (seeds)
# seeds = [5483, 8373]
seeds = [4935, 5539, 4827, 6719, 2357, 6385, 6234, 2913, 7284, 8625]

# List of best solution cut-size calculated in each run
cut_size_list = []

for r in range(run):
    # Generate seed
    seed = seeds[r]

    # Define random solution S0
    S_0 = fun.generate_solution(G.copy(), seed)

    # Draw Original Partitions
    fun.draw_graph(S_0, pos, str(r) + ' - Original Partitions', instance)

    # Apply a given local search algorithm
    S_star = fun.local_search(S_0.copy())

    best_local_solution = S_star

    for gen in range(max_gen):
        print('run: ', r, ' - gen: ', gen)
        
        # Perturb the obtained local optima
        S_first = fun.perturbation(S_star, seed)
        # Apply local search on the perturbed solution #
        S_first_star = fun.local_search(S_first)
        # Accepting criteria
        S_star = fun.accept(S_star, S_first_star)
        
        if fun.cut_size_value(S_star) < fun.cut_size_value(best_local_solution):
            best_local_solution = S_star

    # Draw Final ILS Partitions
    fun.draw_graph(best_local_solution, pos, str(r) + ' - Final ILS Partitions', instance)

    cut_size_list.append(fun.cut_size_value(best_local_solution))

fun.calculate_performance(cut_size_list, instance)
