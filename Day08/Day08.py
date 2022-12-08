import AdventOfCodeBase


class Day08(AdventOfCodeBase.AoCProblem):
    def __init__(self, myInput):
        super().__init__(myInput)
        self.visible = {}
        self.xRange = 0
        self.yRange = 0

    def readInput(self, myInput):
        result = []
        with open(myInput, 'r') as myFile:
            for line in myFile.read().rstrip().split('\n'):
                result.append(line)
        return result

    def parseInput(self, myInput):
        result = []
        for row in myInput:
            result.append(tuple(int(i) for i in row))

        return result

    def p1(self):
        self.xRange = len(self.values[0]) - 1
        self.yRange = len(self.values) - 1
        visible = set()

        greatestTopToBottom = [-1 for _ in range(len(self.values[0]))]
        for y, row in enumerate(self.values):
            greatestLeftToRight = -1
            for x, cell in enumerate(row):
                if cell > greatestLeftToRight:
                    greatestLeftToRight = cell
                    visible.add((x, y))

                if cell > greatestTopToBottom[x]:
                    greatestTopToBottom[x] = cell
                    visible.add((x, y))

        greatestBottomToTop = [-1 for _ in range(len(self.values[0]))]
        for y, row in enumerate(reversed(self.values)):
            greatestRightToLeft = -1
            for x, cell in enumerate(reversed(row)):
                if cell > greatestRightToLeft:
                    greatestRightToLeft = cell
                    visible.add((self.xRange - x, self.yRange - y))

                if cell > greatestBottomToTop[x]:
                    greatestBottomToTop[x] = cell
                    visible.add((self.xRange - x, self.yRange - y))

        return len(visible)

    def p2(self):
        self.xRange = len(self.values[0]) - 1
        self.yRange = len(self.values) - 1
        scores = {}

        greatestTopToBottom = [{i: 0 for i in range(10)} for _ in range(self.xRange+1)]
        for y, row in enumerate(self.values):
            greatestLeftToRight = {i: 0 for i in range(10)}
            for x, cell in enumerate(row):
                scores[(x, y)] = (y - greatestTopToBottom[x][cell]) * (x - greatestLeftToRight[cell])
                for i in range(cell+1):
                    greatestLeftToRight[i] = x
                    greatestTopToBottom[x][i] = y

        greatestBottomToTop = [{i: 0 for i in range(10)} for _ in range(self.xRange+1)]
        for y, row in enumerate(reversed(self.values)):
            greatestRightToLeft = {i: 0 for i in range(10)}
            for x, cell in enumerate(reversed(row)):
                scores[(self.xRange - x, self.yRange - y)] *= (y - greatestBottomToTop[x][cell]) * (x - greatestRightToLeft[cell])
                for i in range(cell+1):
                    greatestRightToLeft[i] = x
                    greatestBottomToTop[x][i] = y

        return max(scores.values())


AdventOfCodeBase.run(Day08, "input.txt")
