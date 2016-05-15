"""
Download the text file here
<http://spark-public.s3.amazonaws.com/algo1/programming_prob/kargerMinCut.txt>.

The file contains the adjacency list representation of a simple
undirected graph. There are 200 vertices labeled 1 to 200. The first
column in the file represents the vertex label, and the particular row
(other entries except the first column) tells all the vertices that the
vertex is adjacent to. So for example, the 6throw looks like : "6 155 56
52 120 ......". This just means that the vertex with label 6 is adjacent
to (i.e., shares an edge with) the vertices with labels
155,56,52,120,......,etc

Your task is to code up and run the randomized contraction algorithm for
the min cut problem and use it on the above graph to compute the min
cut. (HINT: Note that you'll have to figure out an implementation of
edge contractions. Initially, you might want to do this naively,
creating a new graph from the old every time there's an edge
contraction. But you should also think about more efficient
implementations.) (WARNING: As per the video lectures, please make sure
to run the algorithm many times with different random seeds, and
remember the smallest cut that you ever find.)
"""
import random
import copy
import time


class DisjointSet(dict):

    def add(self, item):
        self[item] = item

    def find(self, item):
        parent = self[item]

        while self[parent] != parent:
            parent = self[parent]

        self[item] = parent
        return parent

    def union(self, item1, item2):
        root1 = self.find(item1)
        root2 = self.find(item2)
        self[root2] = root1

    def roots(self):
        roots = set()
        for k in self.keys():
            if self[k] == k:
                roots.add(k)
        return roots


def read_dataset(filename):
    G = {}
    with open(filename, 'rb') as f:
        for l in f:
            labels = l.split()
            G[labels[0]] = labels[1:]
    return G


def contract(G, n1, n2):
    n1_links = G[n1]
    n2_links = G[n2]
    links = filter(lambda x: x != n1 and x != n2, n1_links + n2_links)
    G[n1] = links
    rewrite(G, n2, n1)


def rewrite(G, from_node, to_node):
    for node, edges in G.items():
        for i in range(len(edges)):
            if edges[i] == from_node:
                edges[i] = to_node


def passes(N):
    #n*n*ln(n) => probability is of failure is 1/n
    #but n seems to be enough
    return int(max(10, N))


def karger_min_cut(G):
    cuts = []
    for _ in range(passes(len(G))):
        G_copy = copy.deepcopy(G)
        while len(G_copy) > 2:
            n = random.choice(G_copy.keys())
            n_adj = random.choice(G_copy[n])
            contract(G_copy, n, n_adj)
            del G_copy[n_adj]

        cut = len(G_copy.values()[0])
        cuts.append(cut)
    return min(cuts)


def karger_min_cut_disjoint(G):
    """
    solution using disjoint sets
    """
    cuts = []
    edges = set()
    for n in G.keys():
        for v in G[n]:
            edges.add(tuple(sorted([n, v])))
    edges = list(edges)
    for _ in range(passes(len(G))):
        ds = DisjointSet()
        for n in G.keys():
            ds.add(n)
        random_edges = list(edges)
        random.shuffle(random_edges)
        while len(ds.roots()) > 2:
            (n, v) = random_edges.pop()
            ds.union(n, v)
        cut = 0
        for (n, v) in edges:
            if ds.find(n) != ds.find(v):
                cut += 1
        cuts.append(cut)
    return min(cuts)


def process(filename, mincut_func, expected):
    print "======================="
    G = read_dataset(filename)
    print filename, len(G)
    start = time.time()
    res = mincut_func(G)
    end = time.time()
    print "Method:", mincut_func.__name__, "min cut:", res, "time:", end - start
    assert res == expected

if __name__ == '__main__':
    process('test01.txt', karger_min_cut, 1)
    process('test01.txt', karger_min_cut_disjoint, 1)
    process('kargerMinCut.txt', karger_min_cut, 17)
    process('kargerMinCut.txt', karger_min_cut_disjoint, 17)
