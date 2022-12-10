import AdventOfCodeBase


class Day10(AdventOfCodeBase.AoCProblem):
    def __init__(self, myInput):
        super().__init__(myInput)
        self.x = 1
        self.cycle = {}

    def readInput(self, myInput):
        result = []
        with open(myInput, 'r') as myFile:
            for line in myFile.read().rstrip().split('\n'):
                result.append(line)
        return result

    def p1(self):
        cycle = 1
        for line in self.values:
            if line == 'noop':
                cycle += 1
                self.cycle[cycle] = self.x
            else:
                x = int(line[5:])
                cycle += 2
                self.x += x
                self.cycle[cycle] = self.x

        c = 20
        s = 0
        while c <= cycle:
            try:
                s += self.cycle[c] * c
            except KeyError:
                s += self.cycle[c-1] * c
            c += 40

        return s

    def p2(self):
        self.x = 1
        pixels = []
        cycle = 0
        for line in self.values:
            if line == 'noop':
                self.drawPixel(pixels, cycle)
                cycle += 1

            else:
                x = int(line[5:])
                self.drawPixel(pixels, cycle)
                cycle += 1

                self.drawPixel(pixels, cycle)
                cycle += 1

                self.x += x

        return '\n'.join(' '.join(p) for p in pixels)

    def drawPixel(self, pixels, cycle):
        if cycle % 40 == 0:
            pixels.append([])

        if abs((cycle % 40) - self.x) <= 1:
            pixels[-1].append('#')
        else:
            pixels[-1].append('.')


AdventOfCodeBase.run(Day10, "input.txt")
