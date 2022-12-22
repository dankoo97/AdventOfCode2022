import re
from collections import defaultdict

import AdventOfCodeBase


def adjacent(x, y):
    yield x+1, y
    yield x, y+1
    yield x-1, y
    yield x, y-1


class MonkeyMap:
    def __init__(self):
        self.tiles = set()
        self.walls = set()
        self.connections = defaultdict(dict)
        self.cubeSize = 50
        self.facing = None
        self.position = None

    def walk(self, start, n, cube=None):
        curr = start
        if not cube:
            for i in range(n):
                try:
                    curr = self.connections[curr][self.facing]
                except KeyError:
                    break
            return curr
        else:
            for i in range(n):
                try:
                    curr, facing = self.connections[curr][self.facing]
                    self.facing = facing
                except KeyError:
                    break
            return curr

    def turn(self, direction):
        if direction == 'R':
            self.facing = (self.facing + 1) % 4
        elif direction == 'L':
            self.facing = (self.facing - 1) % 4

    def connect(self):
        self.connections = defaultdict(dict)
        for tile in self.tiles:
            for i, adj in enumerate(adjacent(*tile)):
                if adj in self.tiles:
                    self.connections[tile][i] = adj
                elif adj not in self.walls:
                    poss = None
                    if i == 0:
                        poss = min(t for t in (self.tiles | self.walls) if t[1] == tile[1])
                    elif i == 1:
                        poss = min(t for t in (self.tiles | self.walls) if t[0] == tile[0])
                    elif i == 2:
                        poss = max(t for t in (self.tiles | self.walls) if t[1] == tile[1])
                    elif i == 3:
                        poss = max(t for t in (self.tiles | self.walls) if t[0] == tile[0])

                    if poss not in self.walls:
                        self.connections[tile][i] = poss

    def connectCube(self):
        self.connections = defaultdict(dict)

        for tile in self.tiles:
            x1, y1 = tile
            for i, adj in enumerate(adjacent(*tile)):
                if adj in self.tiles:
                    self.connections[tile][i] = adj, i
                elif adj not in self.walls:
                    poss = None
                    side = (tile[0] // self.cubeSize, tile[1] // self.cubeSize)

                    # Hard code the edges
                    # Shape:
                    #  AB
                    #  C
                    # ED
                    # F
                    #
                    if i == 0:
                        # Right
                        if side == (2, 0):  # B -> D
                            nextSide = (1, 2)
                            facing = 2
                            x2 = (nextSide[0] + 1) * self.cubeSize - 1
                            y2 = (nextSide[1] + 1) * self.cubeSize - 1 - (y1 % self.cubeSize)
                            poss = (x2, y2), facing
                        elif side == (1, 1):  # C -> B
                            nextSide = (2, 0)
                            facing = 3
                            x2 = (nextSide[0]) * self.cubeSize + (y1 % self.cubeSize)
                            y2 = (nextSide[1] + 1) * self.cubeSize - 1
                            poss = (x2, y2), facing
                        elif side == (1, 2):  # D -> B
                            nextSide = (2, 0)
                            facing = 2
                            x2 = (nextSide[0] + 1) * self.cubeSize - 1
                            y2 = (nextSide[1] + 1) * self.cubeSize - 1 - (y1 % self.cubeSize)
                            poss = (x2, y2), facing
                        elif side == (0, 3):  # F -> D
                            nextSide = (1, 2)
                            facing = 3
                            x2 = (nextSide[0]) * self.cubeSize + (y1 % self.cubeSize)
                            y2 = (nextSide[1] + 1) * self.cubeSize - 1
                            poss = (x2, y2), facing

                    elif i == 1:
                        # Down
                        if side == (2, 0):  # B -> C
                            nextSide = (1, 1)
                            facing = 2
                            x2 = (nextSide[0] + 1) * self.cubeSize - 1
                            y2 = (nextSide[1]) * self.cubeSize + (x1 % self.cubeSize)
                            poss = (x2, y2), facing
                        elif side == (1, 2):  # D -> F
                            nextSide = (0, 3)
                            facing = 2
                            x2 = (nextSide[0] + 1) * self.cubeSize - 1
                            y2 = (nextSide[1]) * self.cubeSize + (x1 % self.cubeSize)
                            poss = (x2, y2), facing
                        elif side == (0, 3):  # F -> B
                            nextSide = (2, 0)
                            facing = 1
                            x2 = (nextSide[0]) * self.cubeSize + (x1 % self.cubeSize)
                            y2 = (nextSide[1]) * self.cubeSize
                            poss = (x2, y2), facing

                    elif i == 2:
                        # Left
                        if side == (1, 0):  # A -> E
                            nextSide = (0, 2)
                            facing = 0
                            x2 = (nextSide[0]) * self.cubeSize
                            y2 = (nextSide[1] + 1) * self.cubeSize - 1 - (y1 % self.cubeSize)
                            poss = (x2, y2), facing
                        elif side == (1, 1):  # C -> E
                            nextSide = (0, 2)
                            facing = 1
                            x2 = (nextSide[0]) * self.cubeSize + (y1 % self.cubeSize)
                            y2 = (nextSide[1]) * self.cubeSize
                            poss = (x2, y2), facing
                        elif side == (0, 2):  # E -> A
                            nextSide = (1, 0)
                            facing = 0
                            x2 = (nextSide[0]) * self.cubeSize
                            y2 = (nextSide[1] + 1) * self.cubeSize - 1 - (y1 % self.cubeSize)
                            poss = (x2, y2), facing
                        elif side == (0, 3):  # F -> A
                            nextSide = (1, 0)
                            facing = 1
                            x2 = (nextSide[0]) * self.cubeSize + (y1 % self.cubeSize)
                            y2 = (nextSide[1]) * self.cubeSize
                            poss = (x2, y2), facing

                    elif i == 3:
                        # Up
                        if side == (0, 2):  # E -> C
                            nextSide = (1, 1)
                            facing = 0
                            x2 = (nextSide[0]) * self.cubeSize
                            y2 = (nextSide[1]) * self.cubeSize + (x1 % self.cubeSize)
                            poss = (x2, y2), facing
                        elif side == (1, 0):  # A -> F
                            nextSide = (0, 3)
                            facing = 0
                            x2 = (nextSide[0]) * self.cubeSize
                            y2 = (nextSide[1]) * self.cubeSize + (x1 % self.cubeSize)
                            poss = (x2, y2), facing
                        elif side == (2, 0):  # B -> F
                            nextSide = (0, 3)
                            facing = 3
                            x2 = (nextSide[0]) * self.cubeSize + (x1 % self.cubeSize)
                            y2 = (nextSide[1] + 1) * self.cubeSize - 1
                            poss = (x2, y2), facing
                    if poss[0] not in self.walls:
                        self.connections[tile][i] = poss


class Day22(AdventOfCodeBase.AoCProblem):
    def readInput(self, myInput):
        m = MonkeyMap()
        with open(myInput, 'r') as myFile:
            map, instructions = myFile.read().rstrip().split('\n\n')
            for y, line in enumerate(map.split('\n')):
                for x, c in enumerate(line):
                    if c == '.':
                        m.tiles.add((x, y))
                    elif c == '#':
                        m.walls.add((x, y))
            numberValues = []
            directionValues = []
            for nums in re.split(r'[RL]', instructions.strip()):
                numberValues.append(int(nums))
            for directions in re.split(r'\d+', instructions.strip()):
                directionValues.append(directions)
        return m, list(zip(numberValues, directionValues))

    def p1(self):
        monkeyMap, instructions = self.values
        monkeyMap.connect()
        monkeyMap.facing = 0
        curr = min(monkeyMap.tiles, key=lambda x: (x[1], x[0]))
        for num, turn in instructions:
            monkeyMap.turn(turn)
            curr = monkeyMap.walk(curr, num)

        x, y = curr
        return (y + 1) * 1000 + (x + 1) * 4 + monkeyMap.facing

    def p2(self):
        monkeyMap, instructions = self.values
        monkeyMap.connectCube()
        monkeyMap.facing = 0
        curr = min(monkeyMap.tiles, key=lambda x: (x[1], x[0]))
        for num, turn in instructions:
            monkeyMap.turn(turn)
            curr = monkeyMap.walk(curr, num, True)

        x, y = curr
        return (y + 1) * 1000 + (x + 1) * 4 + monkeyMap.facing


AdventOfCodeBase.run(Day22, 'input.txt')
