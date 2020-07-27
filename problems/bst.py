# makes a BST from an array
class Node:
    def __init__(self, value, left, right):
        self.value = value
        self.left = left
        self.right = right

def bst_from_array(array, start, end):
    if start >= end:
        return None
    mid = (start + end) // 2
    value = array[mid]
    left = bst_from_array(array, start, mid)
    right = bst_from_array(array, mid + 1, end)
    return Node(value, left, right)

def print_bst(start):
    queue = [(start, 0)]
    print('PRINTING')
    while queue:
        node, depth = queue.pop()
        print(' ' * depth + str(node.value))
        if left := node.left:
            queue.append((left, depth + 1))
        if right := node.right:
            queue.append((right, depth + 1))

def make_bst_and_print(num: int):
    bst = bst_from_array(list(range(num)), 0, num)
    print_bst(bst)
