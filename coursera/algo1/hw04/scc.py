"""
The file contains the edges of a directed graph. Vertices are labeled as positive integers from 1 to 875714.
Every row indicates an edge, the vertex label in first column is the tail and the vertex label in second column
is the head (recall the graph is directed, and the edges are directed from the first column vertex to the second
column vertex). So for example, the 11th row looks like : "2 47646". This just means that the vertex with
label 2 has an outgoing edge to the vertex with label 47646

Your task is to code up the algorithm from the video lectures for computing strongly connected components (SCCs),
and to run this algorithm on the given graph.

Output Format: You should output the sizes of the 5 largest SCCs in the given graph,
in decreasing order of sizes, separated by commas (avoid any spaces).
So if your algorithm computes the sizes of the five largest SCCs to be 500, 400, 300, 200 and 100,
then your answer should be "500,400,300,200,100". If your algorithm finds less than 5 SCCs,
then write 0 for the remaining terms. Thus, if your algorithm computes only 3 SCCs whose
sizes are 400, 300, and 100, then your answer should be "400,300,100,0,0".
"""

import sys
import threading
import time
from collections import *


def read_dataset(filename):
    edges = []
    with open(filename, 'rb') as f:
        for l in f:
            data = l.split()
            edges.append(tuple(data))
    return edges


def to_dict_graph(edges):
    G = defaultdict(list)
    for (u, v) in edges:
        G[u].append(v)
    return G


def to_transposed_dict_graph(edges):
    GT = defaultdict(list)
    for (u, v) in edges:
        GT[v].append(u)
    return GT


def dfs_postorder_recr(G, start=None, visited=None):
    if visited is None:
        visited = set()
    order = []

    def visit(s):
        if s in visited: return
        visited.add(s)
        for v in G[s]:
            visit(v)
        order.append(s)

    if start is None:
        nodes = G.keys()
    else:
        nodes = [start]

    for v in nodes:
        visit(v)
    return order


def dfs_postorder_iter(G, start=None, visited=None):
    if start is None:
        nodes = G.keys()
    else:
        nodes = [start]

    if visited is None:
        visited = set()

    stack = []
    order = []

    for v in nodes:
        if v in visited: continue
        visited.add(v)
        stack.append(v)
        while stack:
            v = stack[-1] #peek
            explored = True
            for u in G[v]:
                if u not in visited:
                    explored = False
                    stack.append(u)
                    visited.add(u)
                    break
            if explored:
                v = stack.pop()
                order.append(v)
    return order


def topsort(G, dfs_postorder):
    postorder = dfs_postorder(G)
    postorder.reverse()
    return postorder


def sccs(edges, dfs_postorder):
    G = to_dict_graph(edges)
    GT = to_transposed_dict_graph(edges)
    order = topsort(G, dfs_postorder)

    visited = set()
    sccs = []
    for v in order:
        if v in visited: continue
        scc = dfs_postorder(GT, start=v, visited=visited)
        sccs.append(scc)
    return sorted_result(sccs)


def sccs_recr(edges):
    return sccs(edges, dfs_postorder_recr)


def sccs_iter(edges):
    return sccs(edges, dfs_postorder_iter)


def sccs_nx(edges):
    import networkx as nx
    G = nx.DiGraph()
    for e in edges:
        G.add_edge(*e)
    sccs = nx.strongly_connected_components(G)
    return sorted_result(sccs)


def sorted_result(sccs):
    return sorted(map(lambda scc: len(scc), sccs), reverse=True)[:5]


def process_method(method, edges, sccs_func, expected):
    start = time.time()
    res = sccs_func(edges)
    end = time.time()
    print "Method:", method, "result:", res, "time: ", end - start
    assert res == expected


def process(filename, expected):
    edges = read_dataset(filename)
    print "==================="
    print filename, len(edges)

    process_method("nx", edges, sccs_nx, expected)
    process_method("iterative", edges, sccs_nx, expected)
    process_method("recursive", edges, sccs_nx, expected)

process('test01.txt', [3, 3, 2])
process('test02.txt', [3, 3, 3])

#64MB stack
threading.stack_size(64*1024*1024)
sys.setrecursionlimit(2**31-1)
thread = threading.Thread(target=process, args=('SCC.txt', [434821, 968, 459, 313, 211]))
thread.start()