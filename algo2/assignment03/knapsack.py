"""
In this programming problem and the next you'll code up the knapsack
algorithm from lecture. Let's start with a warm-up. Download the text
file here
<http://spark-public.s3.amazonaws.com/algo2/datasets/knapsack1.txt>.
This file describes a knapsack instance, and it has the following format:
[knapsack_size][number_of_items]
[value_1] [weight_1]
[value_2] [weight_2]
...
For example, the third line of the file is "50074 659", indicating that
the second item has value 50074 and size 659, respectively.

You can assume that all numbers are positive. You should assume that
item weights and the knapsack capacity are integers.

In the box below, type in the value of the optimal solution.
"""
import sys

import functools
import numpy as np
from datetime import datetime


def read_dataset(filename):
    items = []
    with open(filename, 'rb') as f:
        knapsack_size, number_of_items = map(int, f.readline().split())
        for l in f:
            value, weight = map(int, l.split())
            items.append((value, weight))
    assert len(items) == number_of_items
    return knapsack_size, items


def knapsack(knapsack_size, items):
    N, W = len(items), knapsack_size
    table = np.zeros([N + 1, W + 1])

    for i, (value, weight) in enumerate(items, 1):
        for capacity in xrange(W + 1):
            if weight > capacity:
                table[i][capacity] = table[i - 1][capacity]
            else:
                opt1 = table[i - 1][capacity]
                opt2 = table[i - 1][capacity - weight] + value
                table[i][capacity] = max(opt1, opt2)

    solution = []
    i, j = N, W
    while i > 0:
        if table[i][j] != table[i - 1][j]:
            solution.append(items[i - 1])
            j -= items[i - 1][1]
        i -= 1

    solution.reverse()

    #return table[N][W], solution
    return table[N][W]


def knapsack_rec(knapsack_size, items):

    def recurse(i, capacity):
        if i == 0:
            return 0
        value, weight = items[i - 1]
        if weight > capacity:
            return recurse(i - 1, capacity)
        else:
            return max(recurse(i - 1, capacity),  recurse(i - 1, capacity - weight) + value)

    N, W = len(items), knapsack_size
    return recurse(N, W)


def memorized(obj):
    cache = obj.cache = {}

    @functools.wraps(obj)
    def memorizer(*args, **kwargs):
        if args not in cache:
            cache[args] = obj(*args, **kwargs)
        return cache[args]
    return memorizer


def knapsack_rec_mem(knapsack_size, items):
    @memorized
    def recurse(i, capacity):
        if i == 0:
            return 0
        value, weight = items[i - 1]
        if weight > capacity:
            return recurse(i - 1, capacity)
        else:
            return max(recurse(i - 1, capacity),  recurse(i - 1, capacity - weight) + value)

    N, W = len(items), knapsack_size
    return recurse(N, W)


def process(filename, alg_func, expected):
    print "=============="
    knapsack_size, items = read_dataset(filename)
    print filename, "function:", alg_func.__name__, "knapsack size:", knapsack_size, "items:", len(items)
    start = datetime.now()
    res = alg_func(knapsack_size, items)
    end = datetime.now()
    print "Result:", res, "expected:", expected, "time:", end - start
    assert res == expected

sys.setrecursionlimit(15000)
process("knapsack1_test01.txt", knapsack, 60)
process('knapsack1_test01.txt', knapsack_rec, 60)
process('knapsack1_test01.txt', knapsack_rec_mem, 60)

process("knapsack1.txt", knapsack, 2493893)
#process('knapsack1.txt', knapsack_rec, 2493893)
process('knapsack1.txt', knapsack_rec_mem, 2493893)

#process("knapsack_big.txt", knapsack, 4243395)
process('knapsack_big.txt', knapsack_rec_mem, 4243395)
