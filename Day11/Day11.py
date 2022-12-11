import re

import AdventOfCodeBase


class Monkey:
    remainder = 1
    notBrokenWorry = True

    def __init__(self, items, operation, test, results):
        self.items = items
        self.op = lambda old: eval(operation)
        self.operationString = operation
        self.test = test
        self.results = results
        self.otherMonkeys = None
        self.inspections = 0

    def inspect(self):
        self.inspections += 1
        item = self.items.pop(0)
        item = self.op(item)
        if Monkey.notBrokenWorry:
            item //= 3
        item %= Monkey.remainder
        self.otherMonkeys[item % self.test == 0].items.append(item)

    def __repr__(self):
        return f'Monkey(items={str(self.items)})'

    def clone(self):
        m = Monkey([item for item in self.items], self.operationString, self.test, self.results)
        return m


def updateThrows(monkeys):
    for i, monkey in enumerate(monkeys):
        monkeys[i].otherMonkeys = [monkeys[j] for j in monkey.results]


class Day11(AdventOfCodeBase.AoCProblem):
    def readInput(self, myInput):
        result = []
        with open(myInput, 'r') as myFile:
            for line in myFile.read().rstrip().split('\n\n'):
                result.append(line)
        return result

    def parseInput(self, myInput):
        monkeys = []
        for monkey in myInput:
            attributes = monkey.split('\n')
            items = [int(i) for i in re.findall(r'(\d+)', attributes[1])]

            operation = attributes[2].split('=')[1]

            test = int(re.search(r'\d+', attributes[3]).group(0))

            results = [int(i) for i in re.findall(r'\d+', ' '.join(attributes[-2:]))]
            results.reverse()

            monkeys.append(Monkey(items, operation, test, results))

        for monkey in monkeys:
            Monkey.remainder *= monkey.test

        return monkeys

    def p1(self):
        monkeys = [monkey.clone() for monkey in self.values]
        rounds = 20
        updateThrows(monkeys)

        for _ in range(rounds):
            for i, monkey in enumerate(monkeys):
                while monkey.items:
                    monkey.inspect()

        active = [monkey.inspections for monkey in sorted(monkeys, key=lambda monkey: monkey.inspections)]
        return active[-2] * active[-1]

    def p2(self):
        monkeys = [monkey.clone() for monkey in self.values]
        rounds = 10000
        updateThrows(monkeys)

        Monkey.notBrokenWorry = False

        for _ in range(rounds):
            for i, monkey in enumerate(monkeys):
                while monkey.items:
                    monkey.inspect()

        active = [monkey.inspections for monkey in sorted(monkeys, key=lambda monkey: monkey.inspections)]
        return active[-2] * active[-1]


AdventOfCodeBase.run(Day11, 'input.txt')
