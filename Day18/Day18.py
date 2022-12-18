from heapq import heappop, heappush

import AdventOfCodeBase


def adjacent(cube):
    x, y, z = cube
    yield x + 1, y, z
    yield x - 1, y, z
    yield x, y + 1, z
    yield x, y - 1, z
    yield x, y, z + 1
    yield x, y, z - 1


def distance(a, b):
    return sum(abs(i - j) for i, j in zip(a, b))


class Day18(AdventOfCodeBase.AoCProblem):
    def readInput(self, myInput):
        result = set()
        with open(myInput, 'r') as myFile:
            for line in myFile.read().rstrip().split('\n'):
                result.add(tuple(int(i) for i in line.split(',')))

        return result

    def p1(self):
        total = 6 * len(self.values)
        for cube in self.values:
            connected = {*adjacent(cube)}

            total -= len(connected & self.values)

        return total

    def p2(self):
        total = self.p1()
        insideCubes = set()

        # All values are positive therefore 0, 0, 0 is outside
        target = 0, 0, 0
        outsideCubes = {target}

        for cube in self.values:
            for adj in adjacent(cube):
                if adj in self.values:
                    continue
                elif adj in insideCubes:
                    total -= 1
                    continue
                elif adj in outsideCubes:
                    continue

                # Greedy search for outside values
                visited = {adj}
                fringe = [(distance(adj, target), adj)]

                while fringe:
                    _, curr = heappop(fringe)

                    if curr in outsideCubes:
                        outsideCubes |= visited
                        break

                    for other in adjacent(curr):
                        if other not in self.values and other not in visited:
                            visited.add(other)
                            heappush(fringe, (distance(target, other), other))

                if adj not in outsideCubes:
                    total -= 1
                    insideCubes |= visited

        return total


AdventOfCodeBase.run(Day18, 'input.txt')
