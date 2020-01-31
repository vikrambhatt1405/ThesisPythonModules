import networkx as nx
import random
import csv
import numpy as np

def generate_er_graph(n, p):
    g = nx.erdos_renyi_graph(n, p)
    nx.set_edge_attributes(g, None, 'weight')
    for u, v, weight in g.edges.data('weight'):
        if g[v][u]['weight'] is None:
            g[u][v]['weight'] = random.randint(1, 15)
        else:
            g[u][v]['weight'] = g[v][u]['weight']
    return g


def generate_watts_strogatz_graph(n, k, p, seed=123):
    g = nx.connected_watts_strogatz_graph(n, k, p, tries=100, seed=seed)
    nx.set_edge_attributes(g, None, 'weight')
    for u, v, weight in g.edges.data('weight'):
        if g[v][u]['weight'] is None:
            g[u][v]['weight'] = random.randint(1, 15)
        else:
            g[u][v]['weight'] = g[v][u]['weight']
    return g


def generate_albert_barbasi_graph(n, m, seed=123):
    g = nx.barabasi_albert_graph(n, m, seed)
    nx.set_edge_attributes(g, None, 'weight')
    for u, v, weight in g.edges.data('weight'):
        if g[v][u]['weight'] is None:
            g[u][v]['weight'] = random.randint(1, 15)
        else:
            g[u][v]['weight'] = g[v][u]['weight']
    return g


def generate_example_graph():
    g = nx.Graph()
    g.add_edge(0, 1)
    g.add_edge(0, 4)
    g.add_edge(1, 0)
    g.add_edge(1, 4)
    g.add_edge(1, 2)
    g.add_edge(2, 1)
    g.add_edge(2, 3)
    g.add_edge(3, 2)
    g.add_edge(3, 4)
    g.add_edge(4, 0)
    g.add_edge(4, 1)
    g.add_edge(4, 3)
    nx.set_edge_attributes(g, None, 'weight')
    g[0][1]['weight'] = 3
    g[0][4]['weight'] = 2
    g[1][0]['weight'] = 3
    g[1][4]['weight'] = 1
    g[1][2]['weight'] = 2
    g[2][1]['weight'] = 2
    g[2][3]['weight'] = 3
    g[3][2]['weight'] = 3
    g[3][4]['weight'] = 5
    g[4][0]['weight'] = 2
    g[4][1]['weight'] = 1
    g[4][3]['weight'] = 5
    return g


def adjtograph(filename):
    g = nx.Graph()
    with open(filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=' ')
        next(csv_reader)
        # print(next(csv_reader))
        vtx = 0
        for row in csv_reader:
            for adjvtx in row:
                if adjvtx:
                    g.add_edge(vtx, int(adjvtx) - 1, weight=None)
            vtx += 1
        for u, v, weight in g.edges.data('weight'):
            if g[v][u]['weight'] is None:
                g[u][v]['weight'] = random.randint(1, 15)
            else:
                g[u][v]['weight'] = g[v][u]['weight']
    return g

def generate_random_partition(g, seed):
    np.random.seed(seed)
    parts = []
    nodes = np.arange(g.number_of_nodes())
    np.random.shuffle(nodes)
    parts.append(nodes[:g.number_of_nodes()//2])
    parts.append(nodes[g.number_of_nodes()//2:])
    return parts