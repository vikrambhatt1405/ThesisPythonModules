def f(g, partition, alpha, sizeX, sizeY):
    edgecut = 0
    for vtx in range(g.number_of_nodes()):
        partId = partition[vtx]
        for nbr in g.neighbors(vtx):
            if partId != partition[nbr]:
                edgecut += g[vtx][nbr]['weight']
    return float(edgecut / 2) + float(alpha * (sizeX - sizeY) ** 2)
