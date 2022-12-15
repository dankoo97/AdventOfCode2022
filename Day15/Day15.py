import re
from collections import defaultdict
from heapq import heappush, nsmallest, heappop, heappushpop

import AdventOfCodeBase


def distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


class Day15(AdventOfCodeBase.AoCProblem):
    def readInput(self, myInput):
        result = {}
        with open(myInput, 'r') as myFile:
            for line in myFile.read().rstrip().split('\n'):
                match = re.findall(r'-?\d+', line)
                result[tuple(int(i) for i in match[:2])] = tuple(int(i) for i in match[2:])
        return result

    def p1(self):
        y_line = 10
        beacons = set(self.values.values())
        noBeacons = set()

        for sensor, beacon in self.values.items():
            d = distance(sensor, beacon)
            d = d - abs(y_line - sensor[1])

            for x in range(sensor[0] - d, sensor[0] + d + 1):
                noBeacons.add((x, y_line))

        return len(noBeacons - beacons)

    def p2(self):
        y_range = 0, 4000000
        limits = [[] for _ in range(y_range[1] + 1)]

        for sensor, beacon in self.values.items():
            d = distance(sensor, beacon)
            for i, y in enumerate(range(sensor[1] - d, sensor[1])):
                if y_range[0] <= y <= y_range[1]:
                    heappush(limits[y], (sensor[0] - i, sensor[0] + i + 1))

            for i, y in enumerate(range(sensor[1] + d, sensor[1], -1)):
                if y_range[0] <= y <= y_range[1]:
                    heappush(limits[y], (sensor[0] - i, sensor[0] + i + 1))

            if y_range[0] <= sensor[1] <= y_range[1]:
                heappush(limits[sensor[1]], (sensor[0] - d, sensor[0] + d + 1))

        for y in range(y_range[0], y_range[1] + 1):
            start, stop = heappop(limits[y])
            if start > 0:
                return start * 4000000 + y
            while limits[y]:
                nextStart, nextStop = heappop(limits[y])
                if nextStart <= stop:
                    stop = max(nextStop, stop)
                else:
                    return stop * 4000000 + y


AdventOfCodeBase.run(Day15, 'input.txt')
