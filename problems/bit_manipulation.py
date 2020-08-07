# Print the next smallest and next largest number that have the same number
# of 1 bits in their binary representation
def findNextShift(num):
    nextSmallest = nextLargest = None
    prevChar = num & 1
    for i in range(1,32):
        curChar = num & (1 << i)
        if curChar and not prevChar: # ..10..
            nextSmallest = num^(curChar + (1<<(i-1)))
        elif not curChar and prevChar: # ..01..
            nextLargest = num^((1<<i) + prevChar)
        if nextSmallest and nextLargest:
            break
        prevChar = curChar
    print(f'Next smallest: {nextSmallest}\n'
          f'Next largest: {nextLargest}')
