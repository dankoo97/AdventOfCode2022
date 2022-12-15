import AdventOfCodeBase


class Day14(AdventOfCodeBase.AoCProblem):
    start = 500, 0

    def __init__(self, myInput):
        super().__init__(myInput)
        self.rocks = set()
        self.bottom = 0
        self.sand = set()

    def readInput(self, myInput):
        result = []
        with open(myInput, 'r') as myFile:
            for line in myFile.read().rstrip().split('\n'):
                result.append([])
                for coord in line.split(' -> '):
                    a, b = coord.split(',')
                    a = int(a)
                    b = int(b)
                    result[-1].append((a, b))

        return result

    def p1(self):
        for path in self.values:
            for i, coord in enumerate(path[1:]):
                x1, y1 = path[i]
                x2, y2 = coord
                self.bottom = max((self.bottom, y1, y2))
                if x1 == x2:
                    x = x1
                    for y in range(min(y1, y2), max(y1, y2)+1):
                        self.rocks.add((x, y))
                else:
                    y = y1
                    for x in range(min(x1, x2), max(x1, x2)+1):
                        self.rocks.add((x, y))

        current = Day14.start
        path = {}
        while current[1] < self.bottom:
            x, y = current
            if (x, y+1) not in self.rocks | self.sand:
                path[(x, y + 1)] = current
                current = x, y+1
            elif (x-1, y+1) not in self.rocks | self.sand:
                path[(x-1, y + 1)] = current
                current = x-1, y+1
            elif (x+1, y+1) not in self.rocks | self.sand:
                path[(x+1, y + 1)] = current
                current = x+1, y+1
            else:
                self.sand.add(current)
                current = path[current]
        return len(self.sand)

    def p2(self):
        self.bottom = self.bottom + 2
        self.sand = set()
        fringe = {Day14.start}
        visited = set()
        while fringe:
            x, y = fringe.pop()
            visited.add((x, y))

            next = {
                (x, y+1),
                (x-1, y+1),
                (x+1, y+1),
            }

            for pair in next:
                if not (pair in self.rocks or pair in visited or pair in fringe or pair[1] == self.bottom):
                    fringe.add(pair)

        return len(visited)


AdventOfCodeBase.run(Day14, 'input.txt')
