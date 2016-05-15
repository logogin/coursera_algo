"""
In this programming problem you'll code up Dijkstra's shortest-path
algorithm.
Download the text file here
<http://spark-public.s3.amazonaws.com/algo1/programming_prob/dijkstraData.txt>.
(Right click and save link as).
The file contains an adjacency list representation of an undirected
weighted graph with 200 vertices labeled 1 to 200. Each row consists of
the node tuples that are adjacent to that particular vertex along with
the length of that edge. For example, the 6th row has 6 as the first
entry indicating that this row corresponds to the vertex labeled 6. The
next entry of this row "141,8200" indicates that there is an edge
between vertex 6 and vertex 141 that has length 8200. The rest of the
pairs of this row indicate the other vertices adjacent to vertex 6 and
the lengths of the corresponding edges.

Your task is to run Dijkstra's shortest-path algorithm on this graph,
using 1 (the first vertex) as the source vertex, and to compute the
shortest-path distances between 1 and every other vertex of the graph.
If there is no path between a vertex v and vertex 1, we'll define the
shortest-path distance between 1 and vto be 1000000.

You should report the shortest-path distances to the following ten
vertices, in order: 7,37,59,82,99,115,133,165,188,197. You should encode
the distances as a comma-separated string of integers. So if you find
that all ten of these vertices except 115 are at distance 1000 away from
vertex 1 and 115 is 2000 distance away, then your answer should be
1000,1000,1000,1000,1000,2000,1000,1000,1000,1000. Remember the order of
reporting DOES MATTER, and the string should be in the same order in
which the above ten vertices are given. Please type your answer in the
space provided.
"""


import time

DIST_INF = 1000000


def read_dataset(filename):
    G = {}
    with open(filename, 'rb') as f:
        for l in f:
            labels = l.split()
            G[int(labels[0])] = [tuple([int(xx) for xx in x.split(',')]) for x in labels[1:]]
    return G


def dijkstra(G, source):
    dist = {}
    Q = []
    previous = {}
    dist[source] = 0
    for v in G:
        if v != source:
            dist[v] = DIST_INF
            previous[v] = None
        Q.append(v)
    while Q:
        u = min(Q, key=lambda u: dist[u])
        Q.remove(u)

        for (v, length) in G[u]:
            alt = dist[u] + length
            if alt < dist[v]:
                dist[v] = alt
                previous[v] = u
    return dist, previous


def dist_to(dist, vertices):
    result = []
    for v in vertices:
        result.append(dist[v])
    return result


def dijkstra_nx(G, source):
    import networkx as nx
    G_nx = nx.Graph()
    for s, nodes in G.items():
        for node, weight in nodes:
            G_nx.add_edge(s, node, attr_dict={'weight': weight})

    import networkx.algorithms as nx_alg
    previous, dist = nx_alg.dijkstra_predecessor_and_distance(G_nx, source)
    return dist, previous


def dijkstra_scipy(G, source):
    import numpy as np
    import scipy.sparse as sp
    import scipy.sparse.csgraph as csg

    edges = []
    for s, nodes in G.items():
        for node, weight in nodes:
            edges.append((s, node, weight))

    rows, cols, values = zip(*edges)
    csgraph = sp.coo_matrix((values, (rows, cols)), shape=(len(rows), len(cols))).tocsc()
    dist_matrix = csg.dijkstra(csgraph, directed=False)

    dist = {}
    for node in G:
        dist[node] = dist_matrix[source][node]
    return dist, None


def process_method(G, dijkstra_alg, vertices, expected):
    start = time.time()
    dist, _ = dijkstra_alg(G, 1)
    end = time.time()
    res = dist_to(dist, vertices)
    print "Method:", dijkstra_alg.__name__, "result:", res, "time:", end-start
    assert res == expected


def process(filename, vertices, expected):
    print "================="
    G = read_dataset(filename)
    print filename, len(G)

    process_method(G, dijkstra, vertices, expected)
    process_method(G, dijkstra_nx, vertices, expected)
    process_method(G, dijkstra_scipy, vertices, expected)

process("test01.txt", [2,3,4,5,6], [7,9,20,20,11])
process("dijkstraData.txt", [7,37,59,82,99,115,133,165,188,197], [2599,2610,2947,2052,2367,2399,2029,2442,2505,3068])
