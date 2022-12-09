import AdventOfCodeBase


def adjacent(head, tail):
    return abs(tail[0] - head[0]) <= 1 and abs(tail[1] - head[1]) <= 1


class Day09(AdventOfCodeBase.AoCProblem):
    moves = {
        'L': (-1, 0),
        'U': (0, 1),
        'D': (0, -1),
        'R': (1, 0),
    }

    def readInput(self, myInput):
        result = []
        with open(myInput, 'r') as myFile:
            for line in myFile.read().rstrip().split('\n'):
                result.append(line)
        return result

    def p1(self):
        positions = set()
        head = 0, 0
        tail = 0, 0

        for line in self.values:
            direction, distance = line.split()
            distance = int(distance)

            for d in range(distance):
                head = Day09.moves[direction][0] + head[0], Day09.moves[direction][1] + head[1]
                if not adjacent(head, tail):
                    if tail[0] == head[0] or tail[1] == head[1]:
                        tail = ((head[0] - tail[0]) >> 1) + tail[0], ((head[1] - tail[1]) >> 1) + tail[1]
                    else:
                        tail = tail[0] + (1 if head[0] > tail[0] else -1), tail[1] + (1 if head[1] > tail[1] else -1)

                positions.add(tail)

        return len(positions)

    def p2(self):
        positions = []
        knots = [(0, 0) for _ in range(10)]

        for line in self.values:
            direction, distance = line.split()
            distance = int(distance)
            for d in range(distance):
                knots[0] = Day09.moves[direction][0] + knots[0][0], Day09.moves[direction][1] + knots[0][1]
                for i in range(len(knots[1:])):
                    if not adjacent(knots[i], knots[i+1]):
                        if knots[i][0] == knots[i+1][0] or knots[i][1] == knots[i+1][1]:
                            knots[i+1] = ((knots[i][0] - knots[i+1][0]) >> 1) + knots[i+1][0], ((knots[i][1] - knots[i+1][1]) >> 1) + knots[i+1][1],
                        else:
                            knots[i+1] = knots[i+1][0] + (
                                1 if knots[i][0] > knots[i+1][0] else -1
                            ), knots[i+1][1] + (
                                1 if knots[i][1] > knots[i+1][1] else -1
                            )
                if knots[-1] not in positions:
                    positions.append(knots[-1])

        return len(positions)


AdventOfCodeBase.run(Day09, "input.txt")
