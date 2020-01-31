import logging
import sys
import threading
import concurrent.futures
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import matplotlib.pyplot as plt
import nxmetis
import seaborn as sns
from Heurisitc import *
from generate_graph import *
from generate_plots import *

sns.set_style("darkgrid")
"""
Don't worry about these lines if you don't understand what they are doing.Just some helper functions for better
debugging experience.
"""

parser = ArgumentParser("CapsE", formatter_class=ArgumentDefaultsHelpFormatter, conflict_handler='resolve')
logging.basicConfig(filename='errors.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.WARNING)
parser.add_argument("--savefigures", action='store_true', help='Specfiy if you want to save figures')
parser.add_argument("--nodes", default=30, type=int, help="Number of nodes in Erdos-Renyi Graph")
parser.add_argument("--p", default=0.4, type=float, help="Probability of edge being present in Erdos-Renyi Graph")
args = parser.parse_args()

if __name__ == "__main__":
    g = generate_er_graph(args.nodes, args.p)
    options = nxmetis.MetisOptions(dbglvl=nxmetis.enums.MetisDbgLvl.time, niter=1)
    _, parts = nxmetis.partition(G=g, nparts=2, options=options, recursive=False)
    recursive_fiedler_values = nx.algebraic_connectivity(g.subgraph(parts[0])), \
                               nx.algebraic_connectivity(g.subgraph(parts[1]))
    MAX_FIEDLER_VALUEX = -sys.maxsize
    MAX_FIEDLER_VALUEY = -sys.maxsize
    for i in range(100):
        swap_vertices, partition_vector = heurisitc_algorithm(g, parts)
        parts[0] = [vtx for vtx, i in enumerate(partition_vector) if i == 0]
        parts[1] = [vtx for vtx, i in enumerate(partition_vector) if i == 1]
        # print(initial_fiedler_values)
        # print(parts)
        (max_x, max_y) = maximum_fiedler_value_swaps(g, swap_vertices, partition_vector, recursive_fiedler_values)
        # print("Heuristic Bisection: {}".format((max_x, max_y)))
        if MAX_FIEDLER_VALUEX < max_x and MAX_FIEDLER_VALUEY < max_y:
            MAX_FIEDLER_VALUEX = max_x
            MAX_FIEDLER_VALUEY = max_y
    # print("{0}/{1} & {2} & {3:.6g}/{4:.6g} & {5:.6g}/{6:.6g} \\".format(args.nodes, args.p, g.number_of_edges(),
    #                                                                     initial_fiedler_values[0],
    #                                                                     initial_fiedler_values[1],
    #                                                                     MAX_FIEDLER_VALUEX, MAX_FIEDLER_VALUEY))
    max_intit_fiedler_x = MAX_FIEDLER_VALUEX
    max_intit_fiedler_y = MAX_FIEDLER_VALUEY
    # print("{0}/{1}/{2} & {3:.6g}/{4:.6g} \\".format(args.nodes, args.p, g.number_of_edges(), MAX_FIEDLER_VALUEX,
    #                                                 MAX_FIEDLER_VALUEY))
    # print("Recursive Bisection: {}".format(recursive_fiedler_values))
    # ini_parts = generate_random_partition(g)
    # print(ini_parts)
    # ini_fiedler_values = nx.algebraic_connectivity(g.subgraph(ini_parts[0])), \
    #                          nx.algebraic_connectivity(g.subgraph(ini_parts[1]))
    # print(ini_fiedler_values)
    MAX_FIEDLER_VALUEX = -sys.maxsize
    MAX_FIEDLER_VALUEY = -sys.maxsize
    parts = generate_random_partition(g, random.randint(1, 1000000))
    for i in range(100):
        random.seed(i)
        parts = generate_random_partition(g, random.randint(1, g.number_of_nodes()))
        if nx.algorithms.is_connected(g.subgraph(parts[0])) and nx.algorithms.is_connected(g.subgraph(parts[1])):
            break
    initial_fiedler_values = nx.algebraic_connectivity(nx.classes.function.induced_subgraph(g, parts[0])), \
                             nx.algebraic_connectivity(nx.classes.function.induced_subgraph(g, parts[1]))
    # show_partitions(g, parts)
    for i in range(100):
        # print(nx.algorithms.is_connected(nx.classes.function.induced_subgraph(g, parts[0])))
        swap_vertices, partition_vector = heurisitc_algorithm(g, parts)
        parts[0] = [vtx for vtx, i in enumerate(partition_vector) if i == 0]
        parts[1] = [vtx for vtx, i in enumerate(partition_vector) if i == 1]
        # print(initial_fiedler_values)
        # print(parts)
        (max_x, max_y) = maximum_fiedler_value_swaps(g, swap_vertices, partition_vector, initial_fiedler_values)
        # print("Heuristic Bisection: {}".format((max_x, max_y)))
        if MAX_FIEDLER_VALUEX < max_x and MAX_FIEDLER_VALUEY < max_y:
            MAX_FIEDLER_VALUEX = max_x
            MAX_FIEDLER_VALUEY = max_y
    # print("{0}/{1} & {2} & {3:.6g}/{4:.6g} & {5:.6g}/{6:.6g} \\".format(args.nodes, args.p, g.number_of_edges(),
    #                                                                     initial_fiedler_values[0],
    #                                                                     initial_fiedler_values[1],
    #                                                                     MAX_FIEDLER_VALUEX, MAX_FIEDLER_VALUEY))
    print("{0}/{1}/{2} & {3:.6g}/{4:.6g} &{5:6g}/{6:6g} &{7:6g}/{8:6g} \\\\".format(args.nodes, args.p, g.number_of_edges(),
                                                                    initial_fiedler_values[0], initial_fiedler_values[1],
                                                                     MAX_FIEDLER_VALUEX,
                                                                     MAX_FIEDLER_VALUEY, max_intit_fiedler_x,
                                                                     max_intit_fiedler_y))
    # save_results(g, parts, swap_vertices, max_x, max_y)
