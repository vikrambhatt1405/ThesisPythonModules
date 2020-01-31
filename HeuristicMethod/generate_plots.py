from matplotlib import pyplot as plt
import networkx as nx
import numpy as np


def show_partitions(g, parts):
    colormap = ['green'] * g.number_of_nodes()
    for node in parts[0]:
        colormap[node] = 'blue'
    options = {
        'node_size': 250,
        'width': 1, 'with_labels': True}
    plt.figure(figsize=(12, 12))
    plt.subplot(221)
    nx.draw_circular(g, **options, node_color=colormap)
    plt.title("Erdos-Renyi graph:Algebraic Connectivity {:.3f}".format(nx.linalg.algebraic_connectivity(g)))
    plt.subplot(222)
    plt.plot(np.sort(nx.linalg.spectrum.laplacian_spectrum(g)), 'g^', label='Graph Spectrum')
    plt.plot(np.sort(nx.linalg.spectrum.laplacian_spectrum(g.subgraph(parts[0]))), 'r*', label='Component 1 spectrum')
    plt.plot(np.sort(nx.linalg.spectrum.laplacian_spectrum(g.subgraph(parts[1]))), 'b.', label='Component 2 spectrum')
    plt.xlabel('Index')
    plt.ylabel("Eigen Values")
    plt.legend()
    plt.title("Spectrum")

    plt.subplot(223)
    colormap = ['blue'] * len(parts[0])
    nx.draw_circular(g.subgraph(parts[0]), node_color=colormap, **options)
    plt.title("Component 1:Algebraic Connectivity {:.3f}".format(nx.algebraic_connectivity(g.subgraph(parts[0]))))

    plt.subplot(224)
    colormap = ['green'] * len(parts[1])
    nx.draw_circular(g.subgraph(parts[1]), node_color=colormap, **options)
    plt.title(
        "Component 2:Algebraic Connectivity {:.3f}".format(nx.linalg.algebraic_connectivity(g.subgraph(parts[1]))))

    plt.savefig("Erdos-Renyi_" + str(30) + ".png", bbox_inches='tight', transparent=True, frameon=False, pad_inches=0)
    plt.show()


def save_results(g, parts, swap_vertices, max_x, max_y):
    colormap = ['green'] * g.number_of_nodes()
    for node in parts[0]:
        colormap[node] = 'blue'
    options = {
        'node_size': 250,
        'width': 1, 'with_labels': True}
    plt.figure(figsize=(12, 12))
    plt.subplot(221)
    history_x = [i for i, j in swap_vertices]
    history_y = [j for i, j in swap_vertices]
    history_x = np.array(history_x, dtype=np.float)
    history_y = np.array(history_y, dtype=np.float)
    plt.plot(history_x, ":r*", label='Component 1')
    plt.plot(history_y, ":g^", label='Component 2')
    plt.title("Eigenvalues of components found in local search of neighbourhood")
    plt.xlabel("Number of swaps")
    plt.ylabel("Fiedler Value")
    plt.legend()

    plt.subplot(222)
    plt.plot(np.sort(nx.linalg.spectrum.laplacian_spectrum(g.subgraph(parts[0]))), 'r*', label='Component 1 spectrum')
    plt.plot(np.sort(nx.linalg.spectrum.laplacian_spectrum(g.subgraph(parts[1]))), 'b.', label='Component 2 spectrum')
    plt.xlabel('Index')
    plt.ylabel("Eigen Values")
    plt.legend()
    plt.title("Spectrum of output partitioned components")

    plt.subplot(223)
    colormap = ['blue'] * len(parts[0])
    nx.draw_circular(g.subgraph(parts[0]), node_color=colormap, **options)
    plt.title("Component 1:Algebraic Connectivity {:.3f}".format(max_x))

    plt.subplot(224)
    colormap = ['green'] * len(parts[1])
    nx.draw_circular(g.subgraph(parts[1]), node_color=colormap, **options)
    plt.title(
        "Component 2:Algebraic Connectivity {:.3f}".format(max_y))
    plt.savefig("Erdos-Renyi_result" + ".png", bbox_inches='tight', transparent=True,
                frameon=False, pad_inches=0)
    plt.show()
