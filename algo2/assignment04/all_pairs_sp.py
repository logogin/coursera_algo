"""
In this assignment you will implement one or more algorithms for the
all-pairs shortest-path problem. Here are data files describing three
graphs: graph #1
<http://spark-public.s3.amazonaws.com/algo2/datasets/g1.txt>; graph #2
<http://spark-public.s3.amazonaws.com/algo2/datasets/g2.txt>; graph #3
<http://spark-public.s3.amazonaws.com/algo2/datasets/g3.txt>.

The first line indicates the number of vertices and edges, respectively.
Each subsequent line describes an edge (the first two numbers are its
tail and head, respectively) and its length (the third number). NOTE:
some of the edge lengths are negative. NOTE: These graphs may or may not
have negative-cost cycles.

Your task is to compute the "shortest shortest path". Precisely, you
must first identify which, if any, of the three graphs have no negative
cycles. For each such graph, you should compute all-pairs shortest paths
and remember the smallest one (i.e., compute min u,v e Vd(u,v), where
d(u,v) denotes the shortest-path distance from uto v).

If each of the three graphs has a negative-cost cycle, then enter "NULL"
in the box below. If exactly one graph has no negative-cost cycles, then
enter the length of its shortest shortest path in the box below. If two
or more of the graphs have no negative-cost cycles, then enter the
smallest of the lengths of their shortest shortest paths in the box below.

OPTIONAL: You can use whatever algorithm you like to solve this
question. If you have extra time, try comparing the performance of
different all-pairs shortest-path algorithms!

OPTIONAL: If you want a bigger data set to play with, try computing the
shortest shortest path for this graph
<http://spark-public.s3.amazonaws.com/algo2/datasets/large.txt>.
"""
import sys
import numpy as np
from datetime import datetime

import scipy.sparse as sp
import scipy.sparse.csgraph as csg

def read_dataset(filename):
    vertices = set()
    edges = []
    with open(filename, 'rb') as f:
        num_of_vertices, num_of_edges = map(int, f.readline().split())
        for l in f:
            head, tail, weight = map(int, l.split())
            edges.append((head-1, tail-1, weight))
            vertices.add(head-1)
            vertices.add(tail-1)
    assert len(vertices) == num_of_vertices
    assert len(edges) == num_of_edges
    return vertices, edges


def floyd_warshall(vertices, edges):
    V = len(vertices)
    dist = np.empty([V, V], np.int32)
    dist.fill(1000000)
    for v in vertices:
        dist[v, v] = 0

    for u, v, w in edges:
        dist[u, v] = w

    for k in xrange(V):
        for i in xrange(V):
            dist[i, :] = np.amin([dist[i, :], dist[i, k] + dist[k, :]], axis=0)
            if dist[i, i] < 0:
                return None

    np.fill_diagonal(dist, 1000000)
    min_dist = np.amin(dist)
    return min_dist


def numpy_floyd_warshall(vertices, edges):
    graph = to_sparse(edges, len(vertices))
    dist = csg.floyd_warshall(graph)
    np.fill_diagonal(dist, np.nan)
    min_dist = np.nanmin(dist)
    return min_dist


def numpy_bellman_ford(vertices, edges):
    graph = to_sparse(edges, len(vertices))
    dist = csg.bellman_ford(graph)
    np.fill_diagonal(dist, np.nan)
    min_dist = np.nanmin(dist)
    return min_dist


def numpy_johnson(vertices, edges):
    graph = to_sparse(edges, len(vertices))
    dist = csg.johnson(graph)
    np.fill_diagonal(dist, np.nan)
    min_dist = np.nanmin(dist)
    return min_dist


def to_sparse(edges, V):
    rows, cols, values = zip(*edges)
    return sp.coo_matrix((values, (rows, cols)), shape=(V, V)).tocsc()


def max_weight(edges):
    return max(edges, key=lambda x: x[2])


def process(filename, alg_func, expected):
    print "=============="
    vertices, edges = read_dataset(filename)
    print filename, "function:", alg_func.__name__, "vertices:", len(vertices), "edges:", len(edges), "max weight:", max_weight(edges)[2]
    start = datetime.now()
    res = alg_func(vertices, edges)
    end = datetime.now()
    print "Result:", res, "expected:", expected, "time:", end - start
    assert res == expected


def test_numpy(filename, expected):
    algs = [floyd_warshall, numpy_floyd_warshall, numpy_bellman_ford, numpy_johnson]
    print "====== NumPy test ========"
    vertices, edges = read_dataset(filename)
    for alg in algs:
        print filename, "function:", alg.__name__
        start = datetime.now()
        try:
            res = alg(vertices, edges)
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print exc_type
            res = None
        end = datetime.now()
        if res == expected:
            outcome = 'CORRECT'
        else:
            outcome = 'WRONG'
        print "Result:", res, "expected:", expected, "time:", end - start, "-->", outcome

process("g_test01.txt", floyd_warshall, -1)
test_numpy("g_test01.txt", -1)
test_numpy("g_test02.txt", -2)
test_numpy("g_test03.txt", -4)
test_numpy("g_test04.txt", None)
test_numpy("g_test05.txt", -6)
test_numpy("g_test06.txt", 1)
test_numpy("g_test07.txt", None)
test_numpy("g_test08.txt", -3)
test_numpy("g_test09.txt", -5)
test_numpy("g_test10.txt", -9)
test_numpy("g_test11.txt", -8)

process("g1.txt", floyd_warshall, None)
process("g2.txt", floyd_warshall, None)
process("g3.txt", floyd_warshall, -19)

#test_numpy("g3.txt", -19)

#process("large.txt", floyd_warshall, -19)
