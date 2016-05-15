"""
Download the text file here
<http://spark-public.s3.amazonaws.com/algo1/programming_prob/IntegerArray.txt>.

This file contains all of the 100,000 integers between 1 and 100,000
(inclusive) in some order, with no integer repeated.

Your task is to compute the number of inversions in the file given,
where the i-th row of the file indicates the i-th entry of an array.
Because of the large size of this array, you should implement the fast
divide-and-conquer algorithm covered in the video lectures.
"""
def read_dataset(filename):
    nums = []
    with open(filename, 'rb') as f:
        for l in f:
            nums.append(int(l))
    return nums


def merge_and_count(A, left, right):
    i = 0
    j = 0
    k = 0
    count  = 0
    while i < len(left) and j < len(right):
        if left[i] > right[j]:
            A[k] = right[j]
            j += 1
            count += len(left) - i
        else:
            A[k] = left[i]
            i += 1
        k += 1

    while i < len(left):
        A[k] = left[i]
        i += 1
        k += 1

    while j < len(right):
        A[k] = right[j]
        j += 1
        k += 1
    return count


def count_inversions(A):
    N = len(A)
    if N <= 1:
        return 0
    left = A[:N/2]
    right = A[N/2:]
    l = count_inversions(left)
    r = count_inversions(right)
    s = merge_and_count(A, left, right)

    return l + r + s


def process(filename, expected):
    nums = read_dataset(filename)
    print filename, len(nums)
    count = count_inversions(nums)
    print "Result:", count
    assert count == expected

process('test01.txt', 1)
process('IntegerArray.txt', 2407905288)