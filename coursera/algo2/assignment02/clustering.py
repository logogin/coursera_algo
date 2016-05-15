"""
In this programming problem and the next you'll code up the clustering
algorithm from lecture for computing a max-spacing k-clustering.
Download the text file here
<http://spark-public.s3.amazonaws.com/algo2/datasets/clustering1.txt>.
This file describes a distance function (equivalently, a complete graph
with edge costs). It has the following format:

[number_of_nodes]
[edge 1 node 1] [edge 1 node 2] [edge 1 cost]
[edge 2 node 1] [edge 2 node 2] [edge 2 cost]
...
There is one edge (i,j) for each choice of 1<=i<j<=n, where n is the number
of nodes. For example, the third line of the file is "1 3 5250",
indicating that the distance between nodes 1 and 3 (equivalently, the
cost of the edge (1,3)) is 5250. You can assume that distances are
positive, but you should NOT assume that they are distinct.

Your task in this problem is to run the clustering algorithm from
lecture on this data set, where the target number k of clusters is set to
4. What is the maximum spacing of a 4-clustering?
"""

from coursera.algo1.hw03.mincut import DisjointSet


def read_dataset(filename):
    nodes = set()
    edges = []
    with open(filename, 'rb') as f:
        nodes_count = int(f.readline())
        for l in f:
            data = map(int, l.split())
            edges.append(tuple(data))
            nodes.add(data[0])
            nodes.add(data[1])
        assert len(nodes) == nodes_count
        assert range(1, nodes_count + 1) == sorted(nodes)
        return nodes, edges


def kruskal_max_k(nodes, edges, k):
    ds = DisjointSet()
    for node in nodes:
        ds.add(node)
    edges_sorted = sorted(edges, key=lambda x: x[2])
    for (u, v, cost) in edges_sorted:
        if len(ds.roots()) == k:
            # nodes should belong to different clusters
            if ds.find(v) != ds.find(u):
                return cost
            else:
                continue
        if ds.find(v) != ds.find(u):
            ds.union(v, u)
    return "N/A"

if __name__ == '__main__':
    def process(filename, k, expected):
        print "=============="
        nodes, edges = read_dataset(filename)
        print filename, len(nodes)
        res = kruskal_max_k(nodes, edges, k)
        print "Clusters:", k, "result:", res, "expected:", expected
        assert res == expected

    process("clustering1_test01.txt", 4, 134365)
    process("clustering1.txt", 4, 106)