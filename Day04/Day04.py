import AdventOfCodeBase


class Day04(AdventOfCodeBase.AoCProblem):
    def __init__(self, myInput):
        super().__init__(myInput)

    def readInput(self, myInput):
        result = []
        with open(myInput, 'r') as myFile:
            for line in myFile.read().strip().split('\n'):
                result.append(line)
        return result

    def parseInput(self, myInput):
        result = []
        for line in myInput:
            a, b = line.split(',')
            a = set(range(int(a.split('-')[0]), 1 + int(a.split('-')[1])))
            b = set(range(int(b.split('-')[0]), 1 + int(b.split('-')[1])))
            result.append((a, b))
        return result

    def p1(self):
        result = 0
        for a, b in self.values:
            if a <= b or b <= a:
                result += 1
        return result

    def p2(self):
        result = 0
        for a, b in self.values:
            if a & b:
                result += 1
        return result


AdventOfCodeBase.run(Day04, "input.txt")
