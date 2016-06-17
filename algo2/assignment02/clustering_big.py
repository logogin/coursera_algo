"""
In this question your task is again to run the clustering algorithm from
lecture, but on a MUCH bigger graph. So big, in fact, that the distances
(i.e., edge costs) are only defined /implicitly/, rather than being
provided as an explicit list.

The data set is here.
<http://spark-public.s3.amazonaws.com/algo2/datasets/clustering_big.txt>
The format is:
[# of nodes] [# of bits for each node's label]
[first bit of node 1] ... [last bit of node 1]
[first bit of node 2] ... [last bit of node 2]
...
For example, the third line of the file "0 1 1 0 0 1 1 0 0 1 0 1 1 1 1 1
1 0 1 0 1 1 0 1" denotes the 24 bits associated with node #2.

The distance between two nodes u and v in this problem is defined as the
/Hamming distance/--- the number of differing bits --- between the two
nodes' labels. For example, the Hamming distance between the 24-bit
label of node #2 above and the label "0 1 0 0 0 1 0 0 0 1 0 1 1 1 1 1 1
0 1 0 0 1 0 1" is 3 (since they differ in the 3rd, 7th, and 21st bits).

The question is: what is the largest value of k such that there is a
k-clustering with spacing at least 3? That is, how many clusters are
needed to ensure that no pair of nodes with all but 2 bits in common get
split into different clusters?
"""
import itertools
from datetime import datetime

from coursera.algo1.hw03.mincut import DisjointSet


def read_dataset(filename):
    nodes = set()

    with open(filename, 'rb') as f:
        data = map(int, f.readline().split())
        line_num, bits_num = data
        line_count = 0
        for l in f:
            data = ''.join(l.split())
            assert len(data) == bits_num
            nodes.add(int(data, 2))
            line_count += 1
        assert line_count == line_num
    return bits_num, nodes


def create_edges(nodes, bits_num, distance):
    edges = []
    for node in nodes:
        possible_nodes = set(mutations_binary(node, bits_num, distance))
        valid_nodes = nodes.intersection(possible_nodes)
        for v in valid_nodes:
            edges.append((node, v, hamming_binary(node, v)))
    return edges


def kruskal_max_2(nodes, edges):
    ds = DisjointSet()
    for node in nodes:
        ds.add(node)
    edges_sorted = sorted(edges, key=lambda x: x[2])
    for (u, v, cost) in edges_sorted:
        if ds.find(v) != ds.find(u):
            ds.union(v, u)
    return len(ds.roots())


def hamming_binary(a, b):
    return bin(a ^ b).count('1')


def mutations_binary(num, bits_num, hamming_distance):
    for d in range(1, hamming_distance+1):
        for indices in itertools.combinations(range(bits_num), d):
            mutation = num
            for i in indices:
                mutation ^= (1 << i)
            yield mutation


def process(filename, k, expected):
    print "=============="
    bits_num, nodes = read_dataset(filename)
    print filename, "bits:", bits_num, "nodes:", len(nodes)

    start = datetime.now()
    edges = create_edges(nodes, bits_num, k-1)
    end = datetime.now()
    print "edges:", len(edges), "time:", end - start

    start = datetime.now()
    res = kruskal_max_2(nodes, edges)
    end = datetime.now()
    print "Clusters:", k, "result:", res, "expected:", expected, "time:", end - start
    assert res == expected

process('clustering_big_test01.txt', 3, 3)
process('clustering_big.txt', 3, 6118)
