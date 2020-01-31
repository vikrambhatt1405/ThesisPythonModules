import nxmetis
import seaborn as sns
from generate_random_graph import *
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from auxilary_functions import *

sns.set_style("darkgrid")
"""
Don't worry about these lines if you don't understand what they are doing.Just some helper functions for better
debugging experience.
"""

parser = ArgumentParser("CapsE", formatter_class=ArgumentDefaultsHelpFormatter, conflict_handler='resolve')
logging.basicConfig(filename='errors.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.WARNING)
parser.add_argument("--savefigures", action='store_true', help='Specfiy if you want to save figures')
parser.add_argument("--nodes", default=50, type=int, help="Number of nodes in Erdos-Renyi Graph")
parser.add_argument("--p", default=0.25, type=float, help="Probability of edge being present in Erdos-Renyi Graph")
args = parser.parse_args()

if __name__ == "__main__":
    g = generate_er_graph(args.nodes, args.p)
    options = nxmetis.MetisOptions(dbglvl=nxmetis.enums.MetisDbgLvl.time, niter=1)
    _, parts = nxmetis.partition(G=g, nparts=2, options=options, recursive=False)
    recursive_fiedler_values = nx.algebraic_connectivity(g.subgraph(parts[0])), \
                               nx.algebraic_connectivity(g.subgraph(parts[1]))
    print("Recursive Bisection: {}".format(recursive_fiedler_values))
    partition, components = gen_random_partitions(g, parts)
    initial_fiedler_values = (nx.algebraic_connectivity(components[0]), nx.algebraic_connectivity(components[1]))
    swap_nodes_list = get_swap_nodes(g, partition)
    swap_history = swap_nodes(g, swap_nodes_list, partition, components)
    # for i in swap_history:
    #     print(i)
    # print(len(partition[0]), len(partition[1]))
    max_values = get_max_fiedler_values(swap_history, initial_fiedler_values)
    print("Heuristic Bisection: {}".format(max_values))
