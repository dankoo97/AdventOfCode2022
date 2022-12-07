from collections import defaultdict

import AdventOfCodeBase


class Day07 (AdventOfCodeBase.AoCProblem):
    def __init__(self, myInput):
        super().__init__(myInput)
        self.directories = {'/': {}}
        self.sizes = defaultdict(int)
        self.create_directories()

    def readInput(self, myInput):
        result = []
        with open(myInput, 'r') as myFile:
            for line in myFile.read().rstrip().split('\n'):
                result.append(line)
        return result

    def get_directory_size(self, stack):
        c = self.directories
        for p in stack:
            c = c[p]

        result = 0
        for k, v in c.items():
            if isinstance(v, int):
                result += v
            else:
                result += self.get_directory_size((*stack, k))

        return result

    def create_directories(self):
        stack = ['/']
        for line in self.values:
            line = line.strip()
            if line[0] == '$':
                if line[2:4] == 'cd':
                    if line[5:] == '..':
                        stack.pop()
                    elif line[5:] == '/':
                        stack = ['/']
                    else:
                        stack.append(line[5:])
                else:
                    pass
            else:
                a, b = line.split()
                c = self.directories
                for p in stack:
                    c = c[p]

                if a == 'dir':
                    c[b] = {}
                else:
                    c[b] = int(a)
                    for i in range(1, len(stack)+1):
                        self.sizes['/'.join(stack[:i])] += int(a)

    def p1(self):
        return sum(self.sizes[k] for k, v in self.sizes.items() if v <= 100000)

    def p2(self):
        free = 70000000 - self.sizes['/']
        required = 30000000
        return min((v for k, v in self.sizes.items() if free + v >= required))


AdventOfCodeBase.run(Day07, "input.txt")
