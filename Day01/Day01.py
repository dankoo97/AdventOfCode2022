import AdventOfCodeBase


class Day01 (AdventOfCodeBase.AoCProblem):
    def __init__(self, myInput):
        super().__init__(myInput)

    def readInput(self, myInput):
        result = []
        with open(myInput) as myFile:
            result.append([])
            for line in myFile.read().split('\n'):
                if line == '':
                    result.append([])
                else:
                    result[-1].append(int(line))
        return result

    def parseInput(self, myInput):
        return [sum(r) for r in myInput]

    def p1(self):
        return max(self.values)

    def p2(self):
        return sum(sorted(self.values)[-3:])


AdventOfCodeBase.run(Day01, "input.txt")
