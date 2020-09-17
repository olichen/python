# Counts number of ways to make change
def changeCounter(c):
    return changeCounterHelper(c, [25, 10, 5, 1], 0)

def changeCounterHelper(c, denom, i):
    if i == len(denom) - 1:
        if c % denom[i] == 0:
            return 1
        return 0
    ways = 0
    while c >= 0:
        ways += changeCounterHelper(c, denom, i + 1)
        c -= denom[i]
    return ways


# Print combinations of closed/opened parentheses
def getParens(n):
    out = []
    getParensHelper('', n, 0, out)
    return out

def getParensHelper(base, left, right, out):
    if left == 0 and right == 0:
        out.append(base)
        return
    if left > 0:
        getParensHelper(base + '(', left - 1, right + 1, out)
    if right > 0:
        getParensHelper(base + ')', left, right - 1, out)


# Permutation of unique string
def getPermutations(s):
    out = ['']
    for c in s:
        new_out = []
        for o in out:
            for i in range(len(o)+1):
                new_out.append(o[0:i] + c + o[i:len(o)])
        out += new_out
    return out


# Power set
def getSubsets(arr):
    out = [[]]
    for val in arr:
        new_out = []
        for prev_val in out:
            new_val = prev_val.copy()
            new_val.append(val)
            new_out.append(new_val)
        out += new_out
    return out


# Triple step
def tripleStep(n):
    steps = [0, 0, 1]
    for i in range(n):
        steps[i%3] = sum(steps)
    return steps[(n-1)%3]


# Simulate apocalypse
import random

def simulateApocalypse(n):
    m = f = 0
    for i in range(n):
        while random.random() < .5:
            m += 1
        f += 1
    print(f'Men: {m}\nWomen: {f}')

# Check if a linked list is a palindrome
def listIsPalindrome(node) -> bool:
    length = 1
    next_node = node
    while next_node := next_node.next:
        length += 1

    half_p = []
    i = 0
    while i < int(length/2):
        half_p.append(node.data)
        node = node.next
        i = i + 1
    if length % 2:
        node = node.next
        length = length-1
    while i < length:
        if half_p[length - i - 1] != node.data:
            return False
        node = node.next
        i += 1
    return True


# Bare bones linked list
class Node:
    def __init__(self, data, next = None, prev = None):
        self.data = data
        self.next = next
        self.prev = prev


# For an M x N matrix, if an element is 0 set its entire row/column to 0
from typing import List

def zeroMatrix(A: List[list]) -> None:
    M = len(A)
    N = len(A[0])
    m_zero = [False] * M
    n_zero = [False] * N
    for i in range(M):
        for j in range(N):
            if A[i][j] == 0:
                m_zero[i] = True
                n_zero[j] = True
                continue

    for i, zero in enumerate(m_zero):
        if zero:
            for j in range(N):
                A[i][j] = 0

    for j, zero in enumerate(n_zero):
        if zero:
            for i in range(M):
                A[i][j] = 0


# In place rotation of an N x N matrix A by 90 degrees
from typing import List

def rotateMatrix(A: List[list]) -> None:
    N = len(A[0])
    for y in range(int(N/2)):
        ep = N - y - 1 # end pixel
        for x in range(y, ep):
            print(str(y) + ' ' + str(x))
            temp = A[y][y+x]
            A[y][y+x] = A[y+x][ep]
            A[y+x][ep] = A[ep][ep-x]
            A[ep][ep-x] = A[ep-x][y]
            A[ep-x][y] = temp


# Basic string compression ('aabbbc' => 'a2b3c')
def stringCompression(s: str) -> str:
    out = ''
    cur_char = ''
    cur_count = 0
    for c in s:
        if cur_char == c:
            cur_count += 1
        else:
            if cur_count > 1:
                out += str(cur_count)
            out += c
            cur_char = c
            cur_count = 1
    if cur_count > 1:
        out += str(cur_count)
    return out



# Checks whether two strings are permutations of one another
def checkPermutation(s1: str, s2: str) -> bool:
    chars = {}
    for c in s1:
        chars[c] = chars.get(c, 0) + 1
    for c in s2:
        chars[c] = chars.get(c, 0) - 1
    for k, v in chars.items():
        if v != 0:
            return False
    return True


# Checks that all the characters of a string are unique
def isUnique(s: str) -> bool:
    letters = {}
    for c in s:
        if c in letters:
            return False
        letters[c] = True
    return True


# Prints all positive integer solutions to a^3 + b^3 = c^3 + d^3
from collections import defaultdict

def cubedIntegerSum(n: int = 1000) -> None:
    sum_totals = defaultdict(list)
    for a in range(1, n + 1):
        for b in range(1, n + 1):
            total = a**3 + b**3
            sum_totals[total].append((a,b))
    for total, values in sum_totals.items():
        for pair1 in values:
            for pair2 in values:
                print(f'{pair1[0]}, {pair1[1]}, {pair2[0]}, {pair2[1]}')


# Counts the number of pairs of integers in an array a that have difference k
def pairCount(a: list, k: int) -> int:
    value_dict = {}
    count = 0
    for value in a:
        value_dict[value] = True
        if value + k in value_dict:
            count += 1
        if value - k in value_dict:
            count += 1
    print(value_dict)
    return count
