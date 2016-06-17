"""
Download the text file here
<http://spark-public.s3.amazonaws.com/algo1/programming_prob/Median.txt>.

The goal of this problem is to implement the "Median Maintenance"
algorithm (covered in the Week 5 lecture on heap applications). The text
file contains a list of the integers from 1 to 10000 in unsorted order;
you should treat this as a stream of numbers, arriving one by one.
Letting xi denote the ith number of the file, the kth median mk is defined
as the median of the numbers x1,...,xk. (So, if k is odd, then mk is
((k+1)/2)th smallest number among x1,..,xk; if k is even, then mk is the
(k/2)th smallest number among x1,..,xk.)

In the box below you should type the sum of these 10000 medians, modulo
10000 (i.e., only the last 4 digits). That is, you should compute
(m1+m2+m3+...+m10000)mod10000.
"""

import heapq

class MinHeap:
    def __init__(self):
        self.heap = []

    def top(self):
        return self.heap[0]

    def size(self):
        return len(self.heap)

    def push(self, item):
        heapq.heappush(self.heap, item)

    def pop(self):
        return heapq.heappop(self.heap)

class MaxHeap(MinHeap):

    def __init__(self):
        MinHeap.__init__(self)

    def push(self, item):
        MinHeap.push(self, -item)

    def pop(self):
        return -MinHeap.pop(self)

    def top(self):
        return -MinHeap.top(self)


def median(index):
    return (index + 1) // 2 if index % 2 > 0 else index // 2


def kmedian(filename, max_k):
    # simple unbound min-heap
    min_heap = MinHeap()
    # at most m mins as max-heap
    m_mins_heap = MaxHeap()
    count = 0
    sum = 0
    with open(filename, 'rb') as f:
        for k in xrange(1, max_k+1):
            # read next number
            num = int(f.readline())
            min_heap.push(num)

            m = median(k)

            # take m mins
            while m_mins_heap.size() < m:
                min_num = min_heap.pop()
                m_mins_heap.push(min_num)

            # maintain the median property
            while min_heap.size() > 0 and m_mins_heap.top() > min_heap.top():
                max_min_num = m_mins_heap.pop()
                median_min = min_heap.pop()
                min_heap.push(max_min_num)
                m_mins_heap.push(median_min)

            # the top is a median
            mk = m_mins_heap.top()
            sum += mk
    return sum


def process(filename, max_k, expected):
    print "================="
    print filename
    sum = kmedian(filename, max_k)
    print "Result:", sum
    assert sum == expected

process('kmedian_test01.txt', 10, 55)
process('Median.txt', 10000, 46831213)
