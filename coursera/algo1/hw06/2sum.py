"""
Download the text file here
<https://d396qusza40orc.cloudfront.net/algo1%2Fprogramming_prob%2F2sum.txt>.
(Right click and save link as).

The goal of this problem is to implement a variant of the 2-SUM
algorithm (covered in the Week 6 lecture on hash table applications).

The file contains 1 million integers, both positive and negative (there
might be some repetitions!).This is your array of integers, with the
i-th row of the file specifying the i-th entry of the array.

Your task is to compute the number of target values t in the interval
[-10000,10000] (inclusive) such that there are /distinct/ numbers x,y in
the input file that satisfy x+y=t. (NOTE: ensuring distinctness requires
a one-line addition to the algorithm from lecture.)

Write your numeric answer (an integer between 0 and 20001) in the space
provided.
"""

import time
from collections import defaultdict
from collections import Counter

MIN = -10000
MAX = 10000


def read_dataset(filename):
    dataset = []
    with open(filename, 'rb') as f:
        for l in f:
            dataset.append(int(l))
    return dataset


def hash(num):
    # numbers in buckets within [-100,0000, 100,000]
    return abs(num) // (MAX*10)

def create_lookup(nums):
    lookup = defaultdict(set)
    for n in nums:
        key = hash(n)
        lookup[key].add(n)
    return lookup


def find2sum(nums):
    lookup = create_lookup(nums)
    print "Total buckets:", len(lookup)
    result = set()
    counter = Counter()
    for (_, values) in lookup.items():
        size = len(values)
        counter[size] += 1
        if size <= 1: continue
        for x in values:
            for y in values:
                t = x + y
                if MIN <= t <= MAX:
                    result.add(t)
    print "5 most common bucket sizes:", counter.most_common(5)
    mean = sum(map(lambda c: c[0]*c[1], counter.items()))/float(sum(counter.values()))
    print "Mean bucket size:", mean
    return result

def find2sum_naive(nums):
    lookup = set(nums)
    result = set()
    for t in xrange(MIN, MAX+1, 1):
        start = time.time()
        for x in nums:
            y = t - x
            if  y in lookup:
                result.add(t)
    return result

def process(filename, func, expected):
    print "================="
    nums = read_dataset(filename)
    print filename, len(nums)
    start = time.time()
    res = func(nums)
    end = time.time()
    print "Method:", func.__name__, "result:", len(res), "time:", end - start
    assert len(res) == expected

process('2sum_test01.txt', find2sum_naive, 6)
process('2sum_test01.txt', find2sum, 6)
process('algo1-programming_prob-2sum.txt', find2sum, 427)
