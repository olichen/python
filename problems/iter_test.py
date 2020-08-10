class iterator_test:
    def __init__(self):
        self.start = 0

    def __iter__(self):
        self.i = self.start
        return self

    def __next__(self):
        if self.i < 10:
            self.i += 1
            return self.i
        else:
            raise StopIteration
