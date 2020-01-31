import logging
import sys
import numpy as np
import random
import networkx as nx

logging.basicConfig(filename='erros.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.WARNING)
"""
PartitionID is just unique index for each partition. For two partitions partitionID are just 0,1 only
"""


def gen_random_partitions(g, parts):
    partition = {}
    components = {}
    partition[0] = parts[0]
    partition[1] = parts[1]
    logging.info("Random partition created successfully.")
    components[0] = g.subgraph(partition[0]).copy()
    components[1] = g.subgraph(partition[1]).copy()
    return partition, components


def calculate_spectrum(g, components):
    print(nx.algebraic_connectivity(g), nx.algebraic_connectivity(components[0]),
          nx.algebraic_connectivity(components[1]))
    logging.info("Spectrum and algebraic connectivity values calculated.")


# get_ExternalNeighbors reutrns a list of all neighbors in external component
def get_external_neighbors(g, node_id, partition):
    if node_id in partition[0]:
        external_partition_id = 1
    else:
        external_partition_id = 0
    neighbors = set(g[node_id].keys())
    external_neighbors = set(partition[external_partition_id])
    external_neighbors = list(external_neighbors.intersection(neighbors))
    return external_neighbors


def get_internal_neighbors(g, node_id, partition):
    if node_id in partition[0]:
        internal_partition_id = 0
    else:
        internal_partition_id = 1
    neighbors = set(g[node_id].keys())
    internal_neighbors = set(partition[internal_partition_id])
    internal_neighbors = list(internal_neighbors.intersection(neighbors))
    return internal_neighbors


def external_cost(g, node_id, partition):
    external_neighbors = get_external_neighbors(g, node_id, partition)
    cost = 0
    for neighbor in external_neighbors:
        cost += g[node_id][neighbor]['weight']
    return cost


def internal_cost(g, node_id, partition):
    internal_neighbors = get_internal_neighbors(g, node_id, partition)
    cost = 0
    for neighbor in internal_neighbors:
        cost += g[node_id][neighbor]['weight']
    return cost


def get_swap_nodes(g, partition):
    visited_nodes = set()
    swap_nodes = []  # swap nodes in list of tuples of nodes maintained in the same order as they are found.
    for i in range(len(partition[0])):
        max_cost = -sys.maxsize
        target_nodes = []
        for node in set(partition[0]).difference(visited_nodes):
            total_cost = external_cost(g, node, partition) - internal_cost(g, node, partition)
            if total_cost > max_cost:
                target_node = node
        target_nodes.append(target_node)
        max_cost = -sys.maxsize
        for node in set(partition[1]).difference(visited_nodes):
            total_cost = external_cost(g, node, partition) - internal_cost(g, node, partition)
            if total_cost > max_cost:
                target_node = node
        target_nodes.append(target_node)
        visited_nodes.update(target_nodes)
        swap_nodes.append(tuple(target_nodes))
    return swap_nodes


def swap_nodes(g, swap_nodes_list, partition, components):
    swap_history = []
    for (node_x, node_y) in swap_nodes_list:
        partition[0].remove(node_x)
        partition[0].append(node_y)
        partition[1].remove(node_y)
        partition[1].append(node_x)
        components[0] = g.subgraph(partition[0]).copy()
        components[1] = g.subgraph(partition[1]).copy()
        swap_history.append((nx.algebraic_connectivity(components[0]), nx.algebraic_connectivity(components[1])))
    return swap_history


def get_max_fiedler_values(swap_history, initial_fiedler_values):
    max_x, max_y = initial_fiedler_values
    for idx, (i, j) in enumerate(swap_history):
        if i > max_x and j > max_y:
            max_x = i
            max_y = j
    return max_x, max_y
