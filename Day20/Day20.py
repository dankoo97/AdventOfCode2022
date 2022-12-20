import AdventOfCodeBase


# Linked List nodes
class Node:
    def __init__(self, val):
        self.val = val
        self.next = None
        self.prev = None

    def connectNext(self, next):
        self.next = next
        next.prev = self

    def pop(self):
        a, b, c = self.prev, self, self.next
        a.next = c
        c.prev = a
        return a

    def push(self, other):
        a, b, c = self, other, self.next
        a.next = b
        b.prev = a
        b.next = c
        c.prev = b

    def count(self, v):
        curr = self
        for _ in range(abs(v)):
            if v > 0:
                curr = curr.next
            else:
                curr = curr.prev
        return curr

    def order(self):
        stack = [self]
        curr = self.next
        while curr is not self:
            stack.append(curr)
            curr = curr.next
        return stack

    def __str__(self):
        return f'{self.val}'

    def __repr__(self):
        return f'{self.val}'


def mix(order):
    for node in order:
        start = node.pop()
        start.count(node.val % (len(order) - 1)).push(node)


class Day20(AdventOfCodeBase.AoCProblem):
    def readInput(self, myInput):
        a = []
        with open(myInput, 'r') as myFile:
            for line in myFile.read().rstrip().split('\n'):
                a.append(int(line))
        return a

    def p1(self):
        order = [Node(n) for n in self.values]
        zero = None

        for i in range(len(order)):
            order[i - 1].connectNext(order[i])
            if order[i].val == 0:
                zero = order[i]

        mix(order)

        a = zero.count(1000)
        b = a.count(1000)
        c = b.count(1000)

        return a.val + b.val + c.val

    def p2(self):
        decryptionKey = 811589153
        order = [Node(n * decryptionKey) for n in self.values]
        zero = None

        for i in range(len(order)):
            order[i - 1].connectNext(order[i])
            if order[i].val == 0:
                zero = order[i]

        for _ in range(10):
            mix(order)

        a = zero.count(1000)
        b = a.count(1000)
        c = b.count(1000)

        return a.val + b.val + c.val


AdventOfCodeBase.run(Day20, 'input.txt')
