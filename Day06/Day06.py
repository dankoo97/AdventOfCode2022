import AdventOfCodeBase


class Day06(AdventOfCodeBase.AoCProblem):
    def readInput(self, myInput):
        with open(myInput, 'r') as myFile:
            return myFile.read().strip()

    def p1(self):
        s = [c for c in self.values]
        for i, c in enumerate(s, 4):
            if len(set(s[i-4:i])) == 4:
                return i

    def p2(self):
        s = [c for c in self.values]
        for i, c in enumerate(s, 14):
            if len(set(s[i - 14:i])) == 14:
                return i


AdventOfCodeBase.run(Day06, "input.txt")
