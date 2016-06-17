"""
Download the text file here
<http://spark-public.s3.amazonaws.com/algo1/programming_prob/QuickSort.txt>.

The file contains all of the integers between 1 and 10,000 (inclusive,
with no repeats) in unsorted order. The integer in the i-th row of the
file gives you the i-th entry of an input array.

Your task is to compute the total number of comparisons used to sort the
given input file by QuickSort. As you know, the number of comparisons
depends on which elements are chosen as pivots, so we'll ask you to
explore three different pivoting rules.
You should not count comparisons one-by-one. Rather, when there is a
recursive call on a subarray of length m, you should simply add m-1 to
your running total of comparisons. (This is because the pivot element is
compared to each of the other m-1 elements in the subarray in this
recursive call.)

WARNING: The Partition subroutine can be implemented in several
different ways, and different implementations can give you differing
numbers of comparisons. For this problem, you should implement the
Partition subroutine /exactly/ as it is described in the video lectures
(otherwise you might get the wrong answer).
"""


def read_dataset(filename):
    nums = []
    with open(filename, 'rb') as f:
        for l in f:
            nums.append(int(l))
    return nums


def part_first(A, l, r):
    """
    For the first part of the programming assignment, you should always use
    the first element of the array as the pivot element.
    """
    pivot = A[l]
    i = l + 1
    for j in xrange(l + 1, r + 1):
        if A[j] < pivot:
            A[j], A[i] = A[i], A[j]
            i += 1
    A[l], A[i - 1] = A[i - 1], A[l]
    return i - 1


def part_last(A, l, r):
    """
    Compute the number of comparisons (as in Problem 1), always using the
    final element of the given array as the pivot element.
    """
    A[l], A[r] = A[r], A[l]
    return part_first(A, l, r)


def median(A, l, r):
    m = l + (r - l) // 2
    if A[l] > A[r]:
        l, r = r, l
    if A[l] > A[m]:
        m = l
    if A[r] < A[m]:
        m = r
    return m


def median_test():
    print "Test median"
    from itertools import permutations
    perms = permutations([1, 2, 3], 3)
    for p in perms:
        m = median(p, 0, len(p) - 1)
        print p, "median:", p[m]
        assert p[m] == 2


def part_median(A, l, r):
    """
    Compute the number of comparisons (as in Problem 1), using the
    "median-of-three" pivot rule. [The primary motivation behind this rule
    is to do a little bit of extra work to get much better performance on
    input arrays that are nearly sorted or reverse sorted.] In more detail,
    you should choose the pivot as follows. Consider the first, middle, and
    final elements of the given array. (If the array has odd length it
    should be clear what the "middle" element is; for an array with even
    length 2k, use the k-th element as the "middle" element. So for the array
    4 5 6 7, the "middle" element is the second one ---- 5 and not 6!)
    Identify which of these three elements is the median (i.e., the one
    whose value is in between the other two), and use this as your pivot. As
    discussed in the first and second parts of this programming assignment,
    be sure to implement Partition /exactly/ as described in the video
    lectures (including exchanging the pivot element with the first element
    just before the main Partition subroutine).

    EXAMPLE: For the input array 8 2 4 5 7 1 you would consider the first
    (8), middle (4), and last (1) elements; since 4 is the median of the set
    {1,4,8}, you would use 4 as your pivot element.

    SUBTLE POINT: A careful analysis would keep track of the comparisons
    made in identifying the median of the three candidate elements. You
    should NOT do this. That is, as in the previous two problems, you should
    simply add m-1 to your running total of comparisons every time you
    recurse on a subarray with length m.
    """
    m = median(A, l, r)
    A[l], A[m] = A[m], A[l]
    return part_first(A, l, r)


def qsort(A, l=0, r=None, part_func=part_first):
    if r is None:
        r = len(A) - 1
    if (r - l + 1) <= 1:
        return 0

    comp = r - l
    p = part_func(A, l, r)

    comp_left = qsort(A, l, max(0, p - 1), part_func)
    comp_right = qsort(A, min(r, p + 1), r, part_func)

    return comp + comp_left + comp_right

def process(filename, expected):
    nums = read_dataset(filename)
    print "======================="
    print filename, ":", len(nums)
    comp_first = qsort(list(nums), part_func=part_first)
    comp_last = qsort(list(nums), part_func=part_last)
    comp_median = qsort(list(nums), part_func=part_median)
    print "First:", comp_first
    print "Last:", comp_last
    print "Median", comp_median
    assert expected == (comp_first, comp_last, comp_median)

median_test()

process('test01.txt', (9, 12, 9))
process('test02.txt', (45, 37, 25))
process('QuickSort.txt', (162085, 164123, 138382))
