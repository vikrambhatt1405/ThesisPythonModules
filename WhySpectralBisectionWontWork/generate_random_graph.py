import networkx as nx
import random


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