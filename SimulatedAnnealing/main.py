import logging
import sys
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

from stability_function import stability
from generate_graph import *
parser = ArgumentParser("CapsE", formatter_class=ArgumentDefaultsHelpFormatter, conflict_handler='resolve')
logging.basicConfig(filename='errors.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.WARNING)
parser.add_argument("--savefigures", action='store_true', help='Specfiy if you want to save figures')
parser.add_argument("--nodes", default=40, type=int, help="Number of nodes in Erdos-Renyi Graph")
parser.add_argument("--p", default=0.35, type=float, help="Probability of edge being present in Erdos-Renyi Graph")
args = parser.parse_args()

random.seed(123)

if __name__ == "__main__":
    TMax = 100
    TempFact = 0.96
    StopCounter = 0
    NMovements = 0
    SizeFact = 16
    alpha = 0.05
    MinPercentage = 0.02
    counter = 1
    g = generate_er_graph(args.nodes, args.p)
    parts = generate_random_partition(g, counter)
    sizeX = g.number_of_nodes() // 2
    sizeY = g.number_of_nodes() - g.number_of_nodes() // 2
    partition = [0] * g.number_of_nodes()
    for vtx in parts[1]:
        partition[vtx] = 1
    counter += 1
    NVtxs = g.number_of_nodes()

    while True:
        T = TMax
        partX = g.subgraph([vtx for vtx in g.nodes() if partition[vtx] == 0])
        partY = g.subgraph([vtx for vtx in g.nodes() if partition[vtx] == 1])
        # print(partX)
        # for i in partY.nodes():
        # for nbr in partY.neighbors(i):
        # print(partY[i][nbr]['weight'])
        print((nx.linalg.algebraic_connectivity(partX, weight='weight')),
              (nx.linalg.algebraic_connectivity(partY, weight='weight')))
        # del partX, partY
        for i in range(1, SizeFact * NVtxs + 1):
            newPartition = partition.copy()
            random.seed(i)
            selectedVtx_x = random.randint(0, sys.maxsize) % NVtxs
            selectedVtx_y = random.randint(0, sys.maxsize) % NVtxs
            while partition[selectedVtx_x] == partition[selectedVtx_y]:
                selectedVtx_x = random.randint(0, sys.maxsize) % NVtxs
                selectedVtx_y = random.randint(0, sys.maxsize) % NVtxs
            if partition[selectedVtx_x] == 1 and partition[selectedVtx_y] == 0:
                selectedVtx_x, selectedVtx_y = selectedVtx_y, selectedVtx_x
            newPartition[selectedVtx_x] = 1
            newPartition[selectedVtx_y] = 0
            delta = stability(g, newPartition, alpha, sizeX, sizeY) - stability(g, partition, alpha, sizeX, sizeY)
            if delta <= 0:
                partition.clear()
                partition = newPartition
                StopCounter = 0
                NMovements += 1
            elif np.exp(-delta / T) > random.random():
                partition.clear()
                partition = newPartition
                NMovements += 1
            else:
                del newPartition
            print(stability(g, partition, alpha, sizeX, sizeY))
        T = T * TempFact
        acceptedMovements = (SizeFact * NVtxs - NMovements) / SizeFact * NVtxs
        partX = g.subgraph([vtx for vtx in g.nodes() if partition[vtx] == 0]).copy()
        partY = g.subgraph([vtx for vtx in g.nodes() if partition[vtx] == 1]).copy()
        print("Stop Counter:{}".format(StopCounter),
              nx.linalg.algebraic_connectivity(partX),
              nx.linalg.algebraic_connectivity(partY), partX.number_of_nodes(), partY.number_of_nodes())
        del partX, partY
        if acceptedMovements < MinPercentage:
            StopCounter += 1
        if StopCounter == 5:
            break
