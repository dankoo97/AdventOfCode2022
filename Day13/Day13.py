import AdventOfCodeBase


class Packet:
    def __init__(self, values):
        self.values = values

    def __lt__(self, other):
        return compareValues(self.values, other.values)

    def __str__(self):
        return str(self.values)

    def __repr__(self):
        return str(self.values)


def compareValues(left, right):
    # print(left, right)
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return True
        elif left > right:
            return False
        return None
    elif isinstance(left, list) and isinstance(right, list):
        for a, b in zip(left, right):
            result = compareValues(a, b)
            if result is not None:
                return result
        if len(left) < len(right):
            return True
        elif len(left) > len(right):
            return False
        return None
    elif isinstance(left, int):
        left = [left]
    else:
        right = [right]
    return compareValues(left, right)


class Day13(AdventOfCodeBase.AoCProblem):
    def readInput(self, myInput):
        result = []
        with open(myInput, 'r') as myFile:
            for line in myFile.read().rstrip().split('\n\n'):
                result.append(tuple(eval(s) for s in line.split('\n')))
        return result

    def p1(self):
        s = 0
        for i, pairs in enumerate(self.values, 1):
            result = compareValues(*pairs)
            s += i if result else 0

        return s

    def p2(self):
        packets = [Packet([[2]]), Packet([[6]])]
        for pair in self.values:
            packets.append(Packet(pair[0]))
            packets.append(Packet(pair[1]))

        result = [p.values for p in sorted(packets)]

        return (result.index([[2]]) + 1) * (result.index([[6]]) + 1)


AdventOfCodeBase.run(Day13, 'input.txt')
