class AccountCache:
  class _Deque: # doubly linked list
    class _Node: # node that stores ID
      def __init__(self, id, prev = None, next = None):
        self.id = id
        self.prev = prev
        self.next = next

    def __init__(self): # initiate head/tail sentinel nodes
      self.head = self._Node(None)
      self.tail = self._Node(None, self.head)
      self.head.next = self.tail

    def append(self, id): # appends id to the right (tail end) of LL
      node = self._Node(id, self.tail.prev, self.tail)
      self._link(self.tail.prev, node, self.tail)
      return node

    def move_to_right(self, node): # move a node to the right (tail) of LL
      self._link(node.prev, node.next)
      self._link(self.tail.prev, node, self.tail)

    def popleft(self): # pop leftmost node (from head)
      if self.head.next == self.tail:
        raise IndexError('not enough nodes')
      node = self.head.next
      self._link(self.head, node.next)
      return node

    def _link(self, node1, node2, node3 = None): #links together 2 or 3 nodes
      node1.next = node2
      node2.prev = node1
      if node3:
        node2.next = node3
        node3.prev = node2

  def __init__(self, limit): #initializes limit, hash cache, FIFO queue
    self.limit = limit
    self.cache = {} # id: (acc_info, node)
    self.queue = self._Deque() 

  def insert_account_info(self, id, info): # insert into cache and queue
    if id in self.cache:
      node = self.cache[id][1]
      self.queue.move_to_right(node)
      self.cache[id] = (info, node)
    else:
      node = self.queue.append(id)
      self.cache[id] = (info, node)
      if len(self.cache) > self.limit:
        self._delete_lra()

  def _delete_lra(self): # deletes the least recently added item from cache and queue
    node = self.queue.popleft()
    del self.cache[node.id]

  def get_account_info(self, id): # returns the account info, raises error if not found
    if id not in self.cache:
      raise ReferenceError('id not found')
    return self.cache[id][0]
