import networkx as nx


def stability(g, partition, alpha, sizex, sizey):
    inv_stability = 0.0
    part_x = g.subgraph([vtx for vtx in g.nodes() if partition[vtx] == 0]).copy()
    part_y = g.subgraph([vtx for vtx in g.nodes() if partition[vtx] == 1]).copy()
    inv_stability += nx.linalg.algebraic_connectivity(part_x) ** 2 + nx.linalg.algebraic_connectivity(part_y) ** 2
    del part_x, part_y
    return -float(inv_stability) + float(alpha * (sizex - sizey) ** 2)
