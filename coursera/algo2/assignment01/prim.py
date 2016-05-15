"""
In this programming problem you'll code up Prim's minimum spanning tree
algorithm. Download the text file here
<http://spark-public.s3.amazonaws.com/algo2/datasets/edges.txt>. This
file describes an undirected graph with integer edge costs. It has the
format

[number_of_nodes] [number_of_edges]
[one_node_of_edge_1] [other_node_of_edge_1] [edge_1_cost]
[one_node_of_edge_2] [other_node_of_edge_2] [edge_2_cost]
...
For example, the third line of the file is "2 3 -8874", indicating that
there is an edge connecting vertex #2 and vertex #3 that has cost -8874.
You should NOT assume that edge costs are positive, nor should you
assume that they are distinct.

Your task is to run Prim's minimum spanning tree algorithm on this
graph. You should report the overall cost of a minimum spanning tree ---
an integer, which may or may not be negative --- in the box below.

IMPLEMENTATION NOTES: This graph is small enough that the
straightforward O(mn) time implementation of Prim's algorithm should
work fine. OPTIONAL: For those of you seeking an additional challenge,
try implementing a heap-based version. The simpler approach, which
should already give you a healthy speed-up, is to maintain relevant
edges in a heap (with keys = edge costs). The superior approach stores
the unprocessed vertices in the heap, as described in lecture. Note this
requires a heap that supports deletions, and you'll probably need to
maintain some kind of mapping between vertices and their positions in
the heap.
"""

def read_dataset(filename):
    edges = []
    nodes = set()
    with open(filename, 'rb') as f:
        data = map(int, f.readline().split())
        nodes_num, edges_num = data[0], data[1]
        edges_count = 0
        for l in f:
            data = map(int, l.split())
            u, v, cost = data
            edges.append(tuple(data))
            edges_count += 1
            nodes.add(u)
            nodes.add(v)
        assert len(nodes) == nodes_num
        assert edges_count == len(edges)
    return nodes_num, edges

def minimal_spanning_tree(nodes_num, edges):
    tree = set()
    tree_edges = []
    u = edges[0][0]
    tree.add(u)

    while len(tree) != nodes_num:
        crossing_edges = filter(lambda (u, v, _): (u in tree and v not in tree)
            or (u not in tree and v in tree), edges)
        edge = min(crossing_edges, key=lambda (_1, _2, cost): cost)
        tree.add(edge[0])
        tree.add(edge[1])
        tree_edges.append(edge)
    total_cost = sum(map(lambda (_1, _2, cost): cost, tree_edges))
    return total_cost

def process(filename, expected):
    print "=============="
    nodes_num, edges = read_dataset(filename)
    print filename, len(edges)
    res = minimal_spanning_tree(nodes_num, edges)
    print "Result:", res, "expected:", expected
    assert res == expected

process("edges_test01.txt", 2624)
process("edges.txt", -3612829)
