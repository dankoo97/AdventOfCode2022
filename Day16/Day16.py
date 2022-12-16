import itertools
import re
from collections import defaultdict

import AdventOfCodeBase


class Valves:
    def __init__(self, name, rate):
        self.name = name
        self.rate = rate
        self.others = set()

    def addValve(self, other):
        self.others.add(other)
        other.others.add(self)

    def __hash__(self):
        return hash((self.name, self.rate))

    def __lt__(self, other):
        return self.rate < other.rate

    def __repr__(self):
        return self.name


class Day16(AdventOfCodeBase.AoCProblem):
    distances = defaultdict(dict)

    def readInput(self, myInput):
        result = {}
        with open(myInput, 'r') as myFile:
            for line in myFile.read().rstrip().split('\n'):
                rate = re.findall(r'\d+', line)
                others = re.findall(r'[A-Z]{2}', line)
                result[others[0]] = Valves(others[0], int(rate[0])), *others[1:]

        for key in result:
            for other in result[key][1:]:
                try:
                    result[key][0].addValve(result[other][0])
                except TypeError:
                    result[key][0].addValve(result[other])

            result[key] = result[key][0]

        return result

    @staticmethod
    def getDistance(a, b, visited=None):
        if a is b:
            return 0
        if a in Day16.distances and b in Day16.distances[a]:
            return Day16.distances[a][b]
        visited = set() if visited is None else visited
        try:
            result = [Day16.getDistance(other, b, visited | {other}) for other in a.others if other not in visited]
            Day16.distances[a][b] = Day16.distances[b][a] = 1 + min(r for r in result if r is not None)
            return Day16.distances[a][b]
        except ValueError:
            pass

    def p1(self):
        fringe = [(0, 30, self.values['AA'], set())]
        # Lots of valves have 0 rate, therefore don't calculate trying to open them
        valuable = sorted((v for v in self.values.values() if v.rate), reverse=True)
        maxReleased = 0

        # Preprocess route distances
        for v1 in valuable:
            for v2 in valuable:
                Day16.getDistance(v1, v2)

        while fringe:
            # BFS
            released, minutes, current, visited = fringe.pop()
            maxReleased = max(maxReleased, released)

            # Impossible for this state to improve beyond the max, cut it early
            if released + sum(v.rate * minutes for v in valuable if v not in visited) < maxReleased:
                continue

            # Identify next possible states
            for v in valuable:
                if v not in visited:
                    m = minutes - (1 + Day16.getDistance(current, v))
                    if m > 0:
                        r = released + m * v.rate
                        fringe.append((r, m, v, visited | {v}))

        return maxReleased

    def p2(self):
        fringe = [(0, 26, self.values['AA'], set())]
        valuable = sorted((v for v in self.values.values() if v.rate), reverse=True)

        # Keep track of all routes
        routes = defaultdict(int)

        while fringe:
            # BFS
            released, minutes, current, visited = fringe.pop()
            # Pick most released by a given set of visited nodes
            routes[frozenset(visited)] = max(released,  routes[frozenset(visited)])

            for v in valuable:
                if v not in visited:
                    m = minutes - (1 + Day16.getDistance(current, v))
                    if m > 0:
                        r = released + m * v.rate
                        fringe.append((r, m, v, visited | {v}))

        maxReleased = 0

        # Compare each set of visited nodes that do not intersect and find max released sum between them
        for r1, r2 in itertools.combinations(routes.keys(), 2):
            if r1 & r2 == set():
                if routes[r1] + routes[r2] > maxReleased:
                    maxReleased = routes[r1] + routes[r2]

        return maxReleased


AdventOfCodeBase.run(Day16, 'input.txt')
