import re
from collections import defaultdict

import AdventOfCodeBase


class Day05(AdventOfCodeBase.AoCProblem):
    def __init__(self, myInput):
        super().__init__(myInput)

    def readInput(self, myInput):
        result = {}
        with open(myInput, 'r') as myFile:
            crates, instructions = myFile.read().rstrip().split('\n\n')

        result['crates'] = defaultdict(list)

        crates = crates.split('\n')
        for column in range(0, len(crates[-1]), 4):
            for row in range(len(crates)-1):
                try:
                    if crates[row][column+1] != ' ':
                        result['crates'][(column >> 2) + 1].append(crates[row][column+1])
                except IndexError:
                    pass

        result['instructions'] = []
        for line in instructions.split('\n'):
            a, b, c = re.search(r'move (\d+) from (\d+) to (\d+)', line).groups()
            result['instructions'].append(tuple(int(i) for i in (a, b, c)))

        return result

    def p1(self):
        crates = {k: [i for i in v] for k, v in self.values['crates'].items()}
        for a, b, c in self.values['instructions']:
            for i in range(a):
                crate = crates[b].pop(0)
                crates[c].insert(0, crate)
        return ''.join(crates[i][0] for i in range(1, len(crates)+1))

    def p2(self):
        crates = {k: [i for i in v] for k, v in self.values['crates'].items()}
        for a, b, c in self.values['instructions']:
            crate = crates[b][:a]
            crates[b] = crates[b][a:]
            crates[c] = crate + crates[c]
        return ''.join(crates[i][0] for i in range(1, len(crates) + 1))


AdventOfCodeBase.run(Day05, "input.txt")
