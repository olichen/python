def getAdjacentBinary(n: int) -> (int, int):
    return (getPrevBinary(n), getNextBinary(n))


def getPrevBinary(n: int) -> int:
    count = 0
    prev = 1
    i = 0
    while i < 32:
        bit = n >> i & 1
        count += bit
        if bit == 1 and prev == 0:
            out = n & (0xFFFFFFFF << (i + 1))
            out += 0xFFFFFFFF >> (32 - count) << (i - count)
            return out
        prev = bit
        i += 1
    return -1

def getNextBinary(n: int) -> int:
    count = 0
    prev = 0
    i = 0
    while i < 32:
        bit = n >> i & 1
        if bit == 0 and prev == 1:
            out = n & (0xFFFFFFFF << i)
            out += 1 << i
            out += 0xFFFFFFFF >> (33 - count)
            return out
        count += bit
        prev = bit
        i += 1
    return -1
