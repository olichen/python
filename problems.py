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
