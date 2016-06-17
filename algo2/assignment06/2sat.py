"""
In this assignment you will implement one or more algorithms for the
2SAT problem. Here are 6 different 2SAT instances: #1
<https://spark-public.s3.amazonaws.com/algo2/datasets/2sat1.txt> #2
<https://spark-public.s3.amazonaws.com/algo2/datasets/2sat2.txt> #3
<https://spark-public.s3.amazonaws.com/algo2/datasets/2sat3.txt> #4
<https://spark-public.s3.amazonaws.com/algo2/datasets/2sat4.txt> #5
<https://spark-public.s3.amazonaws.com/algo2/datasets/2sat5.txt> #6
<https://spark-public.s3.amazonaws.com/algo2/datasets/2sat6.txt>.

The file format is as follows. In each instance, the number of variables
and the number of clauses is the same, and this number is specified on
the first line of the file. Each subsequent line specifies a clause via
its two literals, with a number denoting the variable and a "-" sign
denoting logical "not". For example, the second line of the first data
file is "-16808 75250", which indicates the clause (not x16808 and x75250).

Your task is to determine which of the 6 instances are satisfiable, and
which are unsatisfiable. In the box below, enter a 6-bit string, where
the ith bit should be 1 if the ith instance is satisfiable, and 0
otherwise. For example, if you think that the first 3 instances are
satisfiable and the last 3 are not, then you should enter the string
111000 in the box below.
"""
import networkx as nx


def read_dataset(filename):
    clauses = []
    variables = set()
    with open(filename, 'rb') as f:
        num_of_variables = int(f.readline().split()[0])
        for l in f:
            x, y = map(int, l.split())
            clauses.append((x, y))
            variables.add(abs(x))
            variables.add(abs(y))
    assert len(clauses) == num_of_variables

    return clauses


def to_graph(clauses):
    G = nx.DiGraph()
    for clause in clauses:
        G.add_edge(-clause[0], clause[1])
        G.add_edge(-clause[1], clause[0])
    return G


def two_sat(clauses):
    G = to_graph(clauses)
    sccs = nx.strongly_connected_components(G)
    for scc in sccs:
        if len(scc) == 1:
            continue
        variables = set(scc)
        for v in scc:
            if -v in variables:
                return False
    return True


def process(filename, expected):
    print "=============="
    clauses = read_dataset(filename)
    print filename, "clauses", len(clauses)
    res = two_sat(clauses)
    print "Result:", res, "expected:", expected
    assert res == expected


process('2sat1.txt', True)
process('2sat2.txt', False)
process('2sat3.txt', True)
process('2sat4.txt', True)
process('2sat5.txt', False)
process('2sat6.txt', False)
