from collections import Counter

import AdventOfCodeBase


class Day23(AdventOfCodeBase.AoCProblem):
    directions = {
        'N': tuple((i, -1) for i in range(-1, 2)),
        'S': tuple((i, 1) for i in range(-1, 2)),
        'W': tuple((-1, i) for i in range(-1, 2)),
        'E': tuple((1, i) for i in range(-1, 2)),
    }

    order = ['N', 'S', 'W', 'E']

    @staticmethod
    def checkDirection(elf, allElves):
        if any((elf[0] + d[0], elf[1] + d[1]) in allElves for d in set.union(*(set(d) for d in Day23.directions.values()))):
            for direction in Day23.order:
                if any((elf[0] + d[0], elf[1] + d[1]) in allElves for d in Day23.directions[direction]):
                    continue
                return direction

    def readInput(self, myInput):
        result = set()
        with open(myInput, 'r') as myFile:
            for y, line in enumerate(myFile.read().rstrip().split('\n')):
                for x, c in enumerate(line):
                    if c == '#':
                        result.add((x, y))
        return result

    @staticmethod
    def draw(elves):
        x1 = min(elves, key=lambda x: x[0])[0]
        x2 = max(elves, key=lambda x: x[0])[0]
        y1 = min(elves, key=lambda x: x[1])[1]
        y2 = max(elves, key=lambda x: x[1])[1]

        s = []

        for y in range(y1, y2+1):
            s.append([])
            for x in range(x1, x2+1):
                if (x, y) in elves:
                    s[-1].append('#')
                else:
                    s[-1].append('.')
            s[-1] = ''.join(s[-1])
        return '\n'.join(s)

    def p1(self):
        rounds = 10
        elves = {e for e in self.values}

        # print(Day23.draw(elves))
        # print('\n\n')

        for _ in range(rounds):
            proposed = {}
            for elf in elves:
                direction = Day23.checkDirection(elf, elves)
                if direction is not None:
                    match direction:
                        case 'N':
                            proposed[elf] = elf[0], elf[1] - 1
                        case 'S':
                            proposed[elf] = elf[0], elf[1] + 1
                        case 'W':
                            proposed[elf] = elf[0] - 1, elf[1]
                        case 'E':
                            proposed[elf] = elf[0] + 1, elf[1]
                else:
                    proposed[elf] = elf

            nextRound = set()
            counter = Counter(proposed.values())
            for elf in proposed:
                if counter[proposed[elf]] == 1:
                    nextRound.add(proposed[elf])
                else:
                    nextRound.add(elf)

            # print(proposed)
            # print(elves)
            # print(nextRound)
            assert len(nextRound) == len(elves)
            # print(Day23.draw(nextRound))
            # print('\n\n')

            elves = nextRound


            Day23.order = [*Day23.order[1:], Day23.order[0]]

        x1 = min(elves, key=lambda x: x[0])[0]
        x2 = max(elves, key=lambda x: x[0])[0]
        y1 = min(elves, key=lambda x: x[1])[1]
        y2 = max(elves, key=lambda x: x[1])[1]

        return ((x2 - x1 + 1) * (y2 - y1 + 1)) - len(elves)

    def p2(self):
        rounds = 0
        elves = {e for e in self.values}

        Day23.order = ['N', 'S', 'W', 'E']

        # print(Day23.draw(elves))
        # print('\n\n')

        while True:
            rounds += 1
            proposed = {}
            for elf in elves:
                direction = Day23.checkDirection(elf, elves)
                if direction is not None:
                    match direction:
                        case 'N':
                            proposed[elf] = elf[0], elf[1] - 1
                        case 'S':
                            proposed[elf] = elf[0], elf[1] + 1
                        case 'W':
                            proposed[elf] = elf[0] - 1, elf[1]
                        case 'E':
                            proposed[elf] = elf[0] + 1, elf[1]
                else:
                    proposed[elf] = elf

            nextRound = set()
            counter = Counter(proposed.values())
            for elf in proposed:
                if counter[proposed[elf]] == 1:
                    nextRound.add(proposed[elf])
                else:
                    nextRound.add(elf)

            # print(proposed)
            # print(elves)
            # print(nextRound)
            assert len(nextRound) == len(elves)
            # print(Day23.draw(nextRound))
            # print('\n\n')

            if elves == nextRound:
                return rounds

            elves = nextRound

            Day23.order = [*Day23.order[1:], Day23.order[0]]




AdventOfCodeBase.run(Day23, 'input.txt')
