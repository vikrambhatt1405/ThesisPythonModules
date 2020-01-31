import numpy as np
import networkx as nx
import random


class vertex_with_gains:
    def __init__(self, vtx, gain):
        self.vtx = vtx
        self.gain = gain


def generate_random_partition(g, seed):
    np.random.seed(seed)
    parts = []
    nodes = np.arange(g.number_of_nodes())
    np.random.shuffle(nodes)
    parts.append(nodes[:g.number_of_nodes()//2])
    parts.append(nodes[g.number_of_nodes()//2:])
    return parts


def external_cost(node, g, binary_part):
    part_id = binary_part[node]
    cost = 0.0
    for nbr in g.neighbors(node):
        if part_id != binary_part[node]:
            cost += g[nbr][node]['weight']
    return cost


def internal_cost(node, g, binary_part):
    part_id = binary_part[node]
    cost = 0.0
    for nbr in g.neighbors(node):
        if part_id == binary_part[nbr]:
            cost += g[nbr][node]['weight']
    return cost


def d(node, g, binary_part):
    return external_cost(node, g, binary_part) - internal_cost(node, g, binary_part)


def swap(dx, j, k):
    temp = dx[j]
    dx[j] = dx[k]
    dx[k] = temp
    return


def update_gains(g, dx, dy, size_x, size_y):
    for i in range(size_x):
        dx[i].gain = dx[i].gain + 2 * g[dx[i].vtx].get(dx[-1].vtx, {'weight': 0})['weight'] - 2 * \
                     g[dx[i].vtx].get(dy[-1].vtx, {'weight': 0})['weight']

    for i in range(size_y):
        dy[i].gain = dy[i].gain + 2 * g[dy[i].vtx].get(dy[-1].vtx, {'weight': 0})['weight'] - 2 * \
                     g[dy[i].vtx].get(dx[-1].vtx, {'weight': 0})['weight']
    return


def maximum_gain_swaps(gains):
    max_sum = gains[0]
    max_pos = 0
    sum = 0
    for idx, i in enumerate(gains):
        sum += i
        if sum > max_sum:
            max_sum = sum
            max_pos = idx
    return max_pos, max_sum


def maximum_fiedler_value_swaps(g, swap_vertices, binary_part, recursive_fiedler_values):
    (max_x, max_y) = recursive_fiedler_values
    for idx, (u, v) in enumerate(swap_vertices):
        binary_part[u] = 1
        binary_part[v] = 0
        part_x = [idx for idx, i in enumerate(binary_part) if i == 0]
        part_y = [idx for idx, i in enumerate(binary_part) if i == 1]
        # print(nx.algebraic_connectivity(g.subgraph(part_x)), nx.algebraic_connectivity(g.subgraph(part_y)))
        if nx.algebraic_connectivity(g.subgraph(part_x)) > max_x and nx.algebraic_connectivity(
                g.subgraph(part_y)) > max_y:
            max_x = nx.algebraic_connectivity(g.subgraph(part_x))
            max_y = nx.algebraic_connectivity(g.subgraph(part_y))
    return max_x, max_y


def heurisitc_algorithm(g, parts):
    binary_part = np.zeros(g.number_of_nodes(), np.int)
    for i in parts[1]:
        binary_part[i] = 1
    size_x = len(parts[0])
    size_y = len(parts[1])
    dx = [vertex_with_gains(vtx, d(vtx, g, binary_part)) for vtx in parts[0]]
    dy = [vertex_with_gains(vtx, d(vtx, g, binary_part)) for vtx in parts[1]]
    swap_vertices = []
    gains = []
    for i in range(g.number_of_nodes() // 2):
        dx.sort(key=lambda x: x.gain, reverse=True)
        dy.sort(key=lambda x: x.gain, reverse=True)
        for j in range(size_x):
            max_gain = dx[0].gain - dy[0].gain - 2 * g[dx[0].vtx].get(dy[0].vtx, {'weight': 0})['weight']
            max_gain_found = False
            for k in range(size_y):
                current_gain = dx[j].gain + dx[k].gain - 2 * g[dx[j].vtx].get(dy[k].vtx, {'weight': 0})['weight']
                if dx[j].gain + dx[k].gain <= max_gain:
                    max_gain_found = True
                    swap_vertices.append((dx[j].vtx, dx[k].vtx))
                    swap(dx, j, -1)
                    swap(dy, k, -1)
                    gains.append(max_gain)
                    break
                elif max_gain <= current_gain:
                    max_gain = current_gain
            if max_gain_found:
                break
        update_gains(g, dx, dy, size_x, size_y)
        size_x -= 1
        size_y -= 1
        if size_x == 0 or size_y == 0:
            break

    # (max_pos, max_sum) = maximum_gain_swaps(gains)
    # print(gains)
    # print(max_pos)
    # print(len(gains))

    # for i in range(max_pos):
    #     binary_part[swap_vertices[i][0]] = 1
    #     binary_part[swap_vertices[i][1]] = 0

    return swap_vertices, binary_part
