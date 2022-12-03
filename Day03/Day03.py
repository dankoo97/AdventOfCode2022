import AdventOfCodeBase


class Day03 (AdventOfCodeBase.AoCProblem):
    def __init__(self, myInput):
        super().__init__(myInput)

    def readInput(self, myInput):
        with open(myInput, 'r') as myFile:
            result = []
            for line in myFile.read().strip().split('\n'):
                result.append(line)
            return result

    def parseInput(self, myInput):
        result = []
        for line in myInput:
            result.append((line[:len(line) >> 1], line[len(line) >> 1:]))
        return result

    def p1(self):
        sum = 0
        for a, b in self.values:
            c = set(a) & set(b)
            sum += 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'.index(c.pop()) + 1
        return sum

    def p2(self):
        sum = 0
        for i in range(0, len(self.values), 3):
            a, b, c = self.values[i:i+3]
            r = {*a[0], *a[1]} & {*b[0], *b[1]} & {*c[0], *c[1]}
            sum += 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'.index(r.pop()) + 1
        return sum


AdventOfCodeBase.run(Day03, "input.txt")
