import math
from collections import defaultdict
from heapq import heappop, heappush

import AdventOfCodeBase


def adjacent(x, y):
    yield x+1, y
    yield x-1, y
    yield x, y+1
    yield x, y-1


def manhattan(x1, y1, x2, y2) -> int:
    return abs(x1 - x2) + abs(y1 - y2)


def draw(player, blizzard, maxX, maxY):
    s = []
    for y in range(maxY+1):
        s.append('#')
        for x in range(maxX+1):
            c = set()
            if blizzard[x, 'down'] & (1 << y):
                c.add('v')
            if blizzard[x, 'up'] & (1 << y):
                c.add('^')
            if blizzard[y, 'left'] & (1 << x):
                c.add('<')
            if blizzard[y, 'right'] & (1 << x):
                c.add('>')
            if (x, y) == player:
                c.add('E')
            if len(c) == 1:
                s[-1] += c.pop()
            elif len(c) == 0:
                s[-1] += '.'
            else:
                s[-1] += str(len(c))
        s[-1] += '#'
    return '\n'.join(s)


def blizzardTick(blizzards, maxX, maxY):
    nextRound = defaultdict(int)
    for n, direction in blizzards.keys():
        match direction:
            case 'up':
                nextRound[n, direction] = (blizzards[n, direction] >> 1) + (blizzards[n, direction] & 1) * (1 << maxY)
            case 'down':
                nextRound[n, direction] = ((blizzards[n, direction] << 1) + (blizzards[n, direction] > (1 << (maxY + 1)))) % ((1 << (maxY + 1)) - 1)
            case 'left':
                nextRound[n, direction] = (blizzards[n, direction] >> 1) + (blizzards[n, direction] & 1) * (1 << maxX)
            case 'right':
                nextRound[n, direction] = ((blizzards[n, direction] << 1) + (blizzards[n, direction] > (1 << (maxX + 1)))) % ((1 << (maxX + 1)) - 1)
    return nextRound


def isBlizzard(player, blizzards):
    a, b = 1 << player[0], 1 << player[1]
    return any((
        a & blizzards[player[1], 'right'],
        a & blizzards[player[1], 'left'],
        b & blizzards[player[0], 'up'],
        b & blizzards[player[0], 'down']
    ))


def generateTicks(blizzard, maxX, maxY):
    multiple = math.lcm((maxX+1), (maxY+1))
    b = [blizzard]
    for _ in range(1, multiple):
        b.append(blizzardTick(b[-1], maxX, maxY))
    return multiple, b


class Day24(AdventOfCodeBase.AoCProblem):
    def readInput(self, myInput):
        walls, blizzard = set(), defaultdict(int)
        maxX, maxY = 0, 0
        with open(myInput, 'r') as myFile:
            for y, line in enumerate(myFile.read().rstrip().split('\n'), -1):
                for x, c in enumerate(line, -1):
                    match c:
                        case '#':
                            walls.add((x, y))
                        case '^':
                            blizzard[x, 'up'] += 1 << y
                            maxY = max(maxY, y)
                            maxX = max(maxX, x)
                        case 'v':
                            blizzard[x, 'down'] += 1 << y
                            maxY = max(maxY, y)
                            maxX = max(maxX, x)
                        case '>':
                            blizzard[y, 'right'] += 1 << x
                            maxY = max(maxY, y)
                            maxX = max(maxX, x)
                        case '<':
                            blizzard[y, 'left'] += 1 << x
                            maxY = max(maxY, y)
                            maxX = max(maxX, x)
        return walls, blizzard, maxX, maxY

    def p1(self):
        start = (0, -1)
        walls, blizzards, maxX, maxY = self.values
        # print(blizzards)
        # print(walls)
        # print(maxX, maxY)

        multiple, allBlizzards = generateTicks(blizzards, maxX, maxY)

        goal = max(walls)
        goal = goal[0]-1, goal[1]

        # print(goal)

        fringe = [(manhattan(*start, *goal), start, (start,))]
        visited = set()

        while fringe:
            score, curr, path = heappop(fringe)

            # print(draw(curr, allBlizzards[(len(path) - 1) % multiple], maxX, maxY))
            # print()

            # print(curr)
            # print(score)
            if curr == goal:
                # print(path)
                return len(path) - 1

            for adj in adjacent(*curr):
                if adj not in walls and adj[1] >= 0 and not isBlizzard(adj, allBlizzards[(len(path)) % multiple]):
                    node = (manhattan(*adj, *goal) + len(path), adj, (*path, adj))
                    if (adj, (len(path) - 1) % multiple) not in visited:
                        visited.add((adj, (len(path) - 1) % multiple))
                        heappush(fringe, node)

            if curr == start or not isBlizzard(curr, allBlizzards[(len(path)) % multiple]):
                node = (manhattan(*adj, *goal) + len(path), curr, (*path, curr))
                if (curr, (len(path) - 1) % multiple) not in visited:
                    visited.add((curr, (len(path) - 1) % multiple))
                    heappush(fringe, node)

        return

    def p2(self):
        start = (0, -1)
        walls, blizzards, maxX, maxY = self.values
        # print(blizzards)
        # print(walls)
        # print(maxX, maxY)

        multiple, allBlizzards = generateTicks(blizzards, maxX, maxY)

        goal = max(walls)
        goal = (goal[0] - 1, goal[1]), start, (goal[0] - 1, goal[1])

        # print(goal)

        fringe = [(manhattan(*start, *goal[0]), start, (start,), 0)]
        visited = set()

        while fringe:
            score, curr, path, g = heappop(fringe)

            # print(draw(curr, allBlizzards[(len(path) - 1) % multiple], maxX, maxY))
            # print()

            # print(curr)
            # print(score)
            if curr == goal[g]:
                # print(g)
                g += 1
                if g == len(goal):
                    return len(path) - 1

            for adj in adjacent(*curr):
                # print(adj)
                # print(walls)
                # print()
                if adj not in walls and -1 <= adj[1] <= maxY + 1 and (adj == start or not isBlizzard(adj, allBlizzards[(len(path)) % multiple])):
                    node = (manhattan(*adj, *goal[g]) + (2 - g) * manhattan(*start, *goal[0]) + len(path), adj, (*path, adj), g)
                    if (adj, (len(path) - 1) % multiple, g) not in visited:
                        visited.add((adj, (len(path) - 1) % multiple, g))
                        heappush(fringe, node)

            if curr == start or not isBlizzard(curr, allBlizzards[(len(path)) % multiple]):
                node = (manhattan(*curr, *goal[g]) + (2 - g) * manhattan(*start, *goal[0]) + len(path), curr, (*path, curr), g)
                if (curr, (len(path) - 1) % multiple, g) not in visited:
                    visited.add((curr, (len(path) - 1) % multiple, g))
                    heappush(fringe, node)
        return


AdventOfCodeBase.run(Day24, 'input.txt')
