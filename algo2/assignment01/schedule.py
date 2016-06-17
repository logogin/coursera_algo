"""
In this programming problem and the next you'll code up the greedy
algorithms from lecture for minimizing the weighted sum of completion
times.. Download the text file here
<http://spark-public.s3.amazonaws.com/algo2/datasets/jobs.txt>. This
file describes a set of jobs with positive and integral weights and
lengths. It has the format

[number_of_jobs]
[job_1_weight] [job_1_length]
[job_2_weight] [job_2_length]
...
For example, the third line of the file is "74 59", indicating that the
second job has weight 74 and length 59. You should NOT assume that edge
weights or lengths are distinct.

Your task in this problem is to run the greedy algorithm that schedules
jobs in decreasing order of the difference (weight - length). Recall
from lecture that this algorithm is not always optimal. IMPORTANT: if
two jobs have equal difference (weight - length), you should schedule
the job with higher weight first. Beware: if you break ties in a
different way, you are likely to get the wrong answer. You should report
the sum of weighted completion times of the resulting schedule --- a
positive integer --- in the box below.
"""

def read_dataset(filename):
    jobs = []
    with open(filename, 'rb') as f:
        jobs_num = int(f.readline())
        for l in f:
            job = map(int, l.split())
            jobs.append(job)
        assert len(jobs) == jobs_num
    return jobs

def cmp_jobs1(job1, job2):
    """
    Your task in this problem is to run the greedy algorithm that schedules
    jobs in decreasing order of the difference (weight - length). Recall
    from lecture that this algorithm is not always optimal. IMPORTANT: if
    two jobs have equal difference (weight - length), you should schedule
    the job with higher weight first. Beware: if you break ties in a
    different way, you are likely to get the wrong answer.
    """
    job1_weight, job1_length = job1
    job2_weight, job2_length = job2
    x_value = job1_weight - job1_length
    y_value = job2_weight - job2_length

    if x_value == y_value:
        return cmp(job1_weight, job2_weight)
    return cmp(x_value, y_value)

def cmp_jobs2(job1, job2):
    """
    For this problem, use the same data set as in the previous problem. Your
    task now is to run the greedy algorithm that schedules jobs (optimally)
    in decreasing order of the ratio (weight/length). In this algorithm, it
    does not matter how you break ties.
    """
    job1_weight, job1_length = job1
    job2_weight, job2_length = job2
    x_value = float(job1_weight)/job1_length
    y_value = float(job2_weight)/job2_length

    return cmp(x_value, y_value)

def schedule(jobs, cmp_func):
    sorted_jobs = sorted(jobs, cmp=cmp_func, reverse=True)
    comp_time = 0
    total_comp_time = 0
    for (weight, length) in sorted_jobs:
        comp_time += length
        total_comp_time += weight * comp_time
    return total_comp_time

def process(filename, cmp_func, expected):
    print "=============="
    jobs = read_dataset(filename)
    print filename, len(jobs)
    res = schedule(jobs, cmp_func)
    print "Method:", cmp_func.__name__, "result:", res, "expected:", expected
    assert res == expected

process("jobs_test01.txt", cmp_jobs1, 145924)
process("jobs_test01.txt", cmp_jobs2, 138232)

process("jobs.txt", cmp_jobs1, 69119377652)
process("jobs.txt", cmp_jobs2, 67311454237)