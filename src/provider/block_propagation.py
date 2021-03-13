import operator
import random
from statistics import mean

import matplotlib.pyplot as plt
import networkx as nx

# run single experiment estimating block propagation time


def estimate_block_propagation_time(n, m):
    # generate graph and compute shortest paths lenghts from node 0 to others
    graph = nx.barabasi_albert_graph(n, m)
    for (u, v, w) in graph.edges(data=True):
        w["weight"] = random.uniform(0.08, 16)
        # print(graph.edges[u,v]['weight'])
    shortest_paths = nx.single_source_dijkstra_path_length(graph, 0)
    return max(shortest_paths.items(), key=operator.itemgetter(1))[1]


# parameter m is how much connection committee member has
m = 3

# k is amount of experiments for averaging
k = 100

ydata = []
xdata = range(20, 200)
for n in xdata:
    data = [estimate_block_propagation_time(n, m) for _ in range(k)]
    # print(n, mean(data))
    ydata.append(mean(data))

plt.plot(xdata, ydata)
plt.ylabel("Propagation Time, Seconds")
plt.xlabel("Committee Size")
plt.show()
