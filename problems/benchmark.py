import timeit
import functools
import random
import cProfile


def testmax(nums):
    high = float('-inf')
    for n in nums:
        high = max(high, n)

def testcomp(nums):
    high = float('-inf')
    for n in nums:
        if n > high:
            high = n

def testcomp2(nums):
    high = float('-inf')
    for n in nums:
        high = n if n > high else high

if __name__ == '__main__':
    nums = list(range(1000))
    random.shuffle(nums)
    t1 = timeit.Timer(functools.partial(testmax, nums))
    t2 = timeit.Timer(functools.partial(testcomp, nums))
    t3 = timeit.Timer(functools.partial(testcomp2, nums))
    print(t1.timeit(10000))
    print(t2.timeit(10000))
    print(t3.timeit(10000))
