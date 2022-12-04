import AdventOfCodeBase


class Day03 (AdventOfCodeBase.AoCProblem):
    def __init__(self, myInput):
        super().__init__(myInput)
        self.map = {c: i for i, c in enumerate('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', 1)}

    def readInput(self, myInput):
        with open(myInput, 'r') as myFile:
            result = []
            for line in myFile.read().strip().split('\n'):
                result.append(line)
            return result

    def p1(self):
        sum = 0
        for line in self.values:
            a, b = line[:len(line) >> 1], line[len(line) >> 1:]
            c = set(a) & set(b)
            sum += self.map[c.pop()]
        return sum

    def p2(self):
        sum = 0
        for i in range(0, len(self.values), 3):
            a, b, c = self.values[i:i+3]
            r = set(a) & set(b) & set(c)
            sum += self.map[r.pop()]
        return sum


AdventOfCodeBase.run(Day03, "input.txt")
