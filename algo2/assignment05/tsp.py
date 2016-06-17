"""
In this assignment you will implement one or more algorithms for the
traveling salesman problem, such as the dynamic programming algorithm
covered in the video lectures. Here is a data file describing a TSP
instance <http://spark-public.s3.amazonaws.com/algo2/datasets/tsp.txt>.
The first line indicates the number of cities. Each city is a point in
the plane, and each subsequent line indicates the x- and y-coordinates
of a single city.

The distance between two cities is defined as the Euclidean distance -
that is, two cities at locations (x,y)and (z,w)have distance
sqrt((x-z)^2+(y-w)^2) between them.
In the box below, type in the minimum cost of a traveling salesman tour
for this instance, /rounded down to the nearest integer/.

HINT: You might experiment with ways to reduce the data set size. For
example, trying plotting the points. Can you infer any structure of the
optimal solution? Can you use that structure to speed up your algorithm?
"""
import math
import matplotlib.pyplot as plt
import itertools
from datetime import datetime
import functools


def read_dataset(filename):
    points = []
    with open(filename, 'rb') as f:
        num_of_points = int(f.readline().split()[0])
        for l in f:
            x, y = map(float, l.split())
            points.append((x, y))
    assert len(points) == num_of_points

    return points


def dist(p, q):
    return math.sqrt((p[0]-q[0]) ** 2 + (p[1]-q[1]) ** 2)


def total_dist_closed(start, tour):
    return dist(start, tour[0]) + sum([dist(tour[i], tour[i+1]) for i, p in enumerate(tour[:-1])]) + dist(tour[-1], start)


def tsp_bruteforce(points):
    start = points[0]
    tour = min([perm for perm in itertools.permutations(points[1:])], key=lambda perm: total_dist_closed(start, perm))
    return total_dist_closed(start, tour)


def memorized(obj):
    cache = obj.cache = {}

    @functools.wraps(obj)
    def memorizer(*args, **kwargs):
        if args not in cache:
            cache[args] = obj(*args, **kwargs)
        return cache[args]
    return memorizer


def tsp_rec(points):
    start = points[0]

    @memorized
    def recurse(s, tour):
        if tour:
            return min(dist(p, s) + recurse(p, tour - {p}) for p in tour)
        else:
            return dist(start, s)

    return recurse(start, frozenset(points[1:]))


"""
http://www.geeksforgeeks.org/travelling-salesman-problem-set-1/
If size of S is 2, then S must be {1, i},
 C(S, i) = dist(1, i)
Else if size of S is greater than 2.
 C(S, i) = min { C(S-{i}, j) + dis(j, i)} where j belongs to S, j != i and j != 1.
 Result is min {C(S{1,n}, j) + dis(j, 1)}
"""
def tsp_dynamic(points):
    start = 0
    other_points = range(1, len(points))
    state = dict()
    dists = [[dist(x, y) for y in points] for x in points]

    for i in other_points:
        state[(frozenset([i]), i)] = dists[start][i]

    for set_size in range(2, len(points)):
        next_state = dict()
        for c in itertools.combinations(other_points, set_size):
            S = frozenset(c)
            for i in S:
                next_state[(S, i)] = min([state[(S - {i}, j)] + dists[i][j] for j in S if i != j])
        state = next_state
    res = min([state[(frozenset(other_points), j)] + dists[j][start] for j in other_points])
    return res


def tsp_final_rec(points):
    return tsp_rec(points[:13]) + tsp_rec(points[11:]) - 2*dist(points[11], points[12])


def tsp_final_dynamic(points):
    return tsp_dynamic(points[:13]) + tsp_dynamic(points[11:]) - 2*dist(points[11], points[12])


def plot_points(title, points):
    x, y = zip(*points)
    plt.title(title)
    plt.scatter(x, y)

    for i, p in enumerate(points):
        plt.annotate(i, p)
    plt.savefig(title + ".png")


def process(filename, alg_func, expected):
    print "=============="
    points = read_dataset(filename)
    print filename, "function:", alg_func.__name__, "points", len(points)
    start = datetime.now()
    res = alg_func(points)
    res = round(res, 4)
    end = datetime.now()
    print "Result:", res, "expected:", expected, "time:", end - start
    assert res == expected


process('tsp_test01.txt', tsp_bruteforce, 4)
process('tsp_test01.txt', tsp_rec, 4)
process('tsp_test01.txt', tsp_dynamic, 4)

process('tsp_test02.txt', tsp_bruteforce, 10.4721)
process('tsp_test02.txt', tsp_rec, 10.4721)
process('tsp_test02.txt', tsp_dynamic, 10.4721)

process('tsp_test04.txt', tsp_bruteforce, 124.9659)
process('tsp_test04.txt', tsp_rec, 124.9659)
process('tsp_test04.txt', tsp_dynamic, 124.9659)

process('tsp_test05.txt', tsp_bruteforce, 6.1799)
process('tsp_test05.txt', tsp_rec, 6.1799)
process('tsp_test05.txt', tsp_dynamic, 6.1799)

process('tsp_test06.txt', tsp_bruteforce, 6.2653)
process('tsp_test06.txt', tsp_rec, 6.2653)
process('tsp_test06.txt', tsp_dynamic, 6.2653)

process('tsp_test07.txt', tsp_bruteforce, 124.9659)
process('tsp_test07.txt', tsp_rec, 124.9659)
process('tsp_test07.txt', tsp_dynamic, 124.9659)

process('tsp_test03.txt', tsp_rec, 16898.1335)
process('tsp_test03.txt', tsp_dynamic, 16898.1335)

points = read_dataset('tsp.txt')
plot_points('tsp.txt', points)
process('tsp.txt', tsp_final_rec, 26442.7303)
process('tsp.txt', tsp_final_dynamic, 26442.7303)
