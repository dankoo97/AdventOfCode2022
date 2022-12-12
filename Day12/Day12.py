from collections import defaultdict
from heapq import heappush, heappop

import AdventOfCodeBase


def adjacent(x, y):
    yield x+1, y
    yield x-1, y
    yield x, y+1
    yield x, y-1


class Day12(AdventOfCodeBase.AoCProblem):
    def readInput(self, myInput):
        result = []
        with open(myInput, 'r') as myFile:
            for line in myFile.read().rstrip().split('\n'):
                result.append(list(line))

        return result

    def p1(self):
        fringe = []
        visited = set()
        goal = None
        maxX = -1
        maxY = len(self.values)
        helper = defaultdict(set)  # Track all locations for each letter

        for y, line in enumerate(self.values):
            maxX = max((len(line), maxX))
            for x, c in enumerate(line):
                if c == 'S':
                    heappush(fringe, (0, (x, y), 0))
                    self.values[y][x] = 'a'
                elif c == 'E':
                    goal = x, y
                    self.values[y][x] = 'z'
                helper[self.values[y][x]].add((x, y))

        while fringe:
            _, current, history = heappop(fringe)
            letter = self.values[current[1]][current[0]]
            nextLetter = chr(ord(letter) + 1)

            if current == goal:
                self.values[goal[1]][goal[0]] = 'E'  # reset for part 2
                return history

            for x, y in adjacent(*current):
                if x < 0 or y < 0 or x >= maxX or y >= maxY or (x, y) in visited:
                    continue

                if abs(ord(letter) + 1 >= ord(self.values[y][x])):
                    visited.add((x, y))
                    if letter != 'z':
                        hFunc = min(abs(h[0] - current[0]) + abs(h[1] - current[1]) for h in helper[nextLetter])  # find closest next letter
                        heappush(fringe, (history + hFunc, (x, y), history + 1))
                    else:
                        heappush(fringe, (history + abs(goal[0] - current[0]) + abs(goal[1] - current[1]), (x, y), history + 1))
        return

    def p2(self):
        goal = None
        maxX = -1
        maxY = len(self.values)
        helper = defaultdict(set)
        fringe = []
        visited = set()

        for y, line in enumerate(self.values):
            maxX = max((len(line), maxX))
            for x, c in enumerate(line):
                if c == 'a':
                    heappush(fringe, (0, (x, y), 0))
                elif c == 'E':
                    goal = x, y
                helper[self.values[y][x]].add((x, y))

        while fringe:
            _, current, history = heappop(fringe)
            letter = self.values[current[1]][current[0]]
            nextLetter = chr(ord(letter) + 1)

            if current == goal:
                # Found
                # Weird off by one error, unsure where it comes up
                return history + 1

            for x, y in adjacent(*current):
                if x < 0 or y < 0 or x >= maxX or y >= maxY or (x, y) in visited:
                    continue

                if abs(ord(letter) + 1 >= ord(self.values[y][x])):
                    visited.add((x, y))
                    if letter != 'z':
                        hFunc = min(abs(h[0] - current[0]) + abs(h[1] - current[1]) for h in helper[nextLetter])
                        heappush(fringe, (history + hFunc, (x, y), history + 1))
                    else:
                        heappush(fringe, (history + abs(goal[0] - current[0]) + abs(goal[1] - current[1]), (x, y), history + 1))

        # return min(paths.values())


AdventOfCodeBase.run(Day12, "input.txt")
