import AdventOfCodeBase


class Monkey:
    monkeys = {}

    def __init__(self, name, op):
        self.name = name
        self.op = op
        self.func = None
        self.a = None
        self.b = None
        Monkey.monkeys[name] = self

    def __repr__(self):
        return f'Monkey({self.name}, {self.op})'

    def __str__(self):
        return f'{self.func()}'

    def substitute(self, f):
        """
        Visualization function
        :param f: A list displaying the function
        :return: List after substituting for the variable
        """
        marked = set()
        for i, val in enumerate(f):
            if val == self.name:
                marked.add(i)
        for i in marked:
            f = f[:i] + ['('] + self.op.strip().split() + [')'] + f[i + 1:]
        return f

    @staticmethod
    def connect():
        """
        Connects the existing monkeys based on their function and name, tries to use function so that values can change
        :return:
        """
        for monkey in Monkey.monkeys:
            if Monkey.monkeys[monkey].op.isdigit():
                Monkey.monkeys[monkey].func = lambda myMonkey=Monkey.monkeys[monkey]: int(myMonkey.op)
                continue

            a, op, b = Monkey.monkeys[monkey].op.split()
            Monkey.monkeys[monkey].a = Monkey.monkeys[a]
            Monkey.monkeys[monkey].b = Monkey.monkeys[b]

            if op == '+':
                def add(a=a, b=b):
                    return Monkey.monkeys[a].func() + Monkey.monkeys[b].func()

                Monkey.monkeys[monkey].func = add
            elif op == '-':
                def sub(a=a, b=b):
                    return Monkey.monkeys[a].func() - Monkey.monkeys[b].func()

                Monkey.monkeys[monkey].func = sub
            elif op == '*':
                def mult(a=a, b=b):
                    return Monkey.monkeys[a].func() * Monkey.monkeys[b].func()

                Monkey.monkeys[monkey].func = mult
            elif op == '/':
                def div(a=a, b=b):
                    return Monkey.monkeys[a].func() // Monkey.monkeys[b].func()

                Monkey.monkeys[monkey].func = div


class Day21(AdventOfCodeBase.AoCProblem):
    def readInput(self, myInput):
        with open(myInput, 'r') as myFile:
            for line in myFile.read().rstrip().split('\n'):
                name, op = line.split(':')
                Monkey(name, op.strip())

    def p1(self):
        Monkey.connect()
        return Monkey.monkeys['root'].func()

    def p2(self):
        reverseMap = {}

        def solve(monkey):
            """
            Reverses the functions to solve for humn
            :param monkey: The current monkey to solve
            :return: The correct value for human
            """

            if monkey.name == 'humn':
                return reverseMap['root']

            _, op, _ = monkey.op.strip().split()

            try:
                # If we can solve left half of function
                a = monkey.a.func()
                reverseMap[monkey.a.name] = a

                # Left half reverse
                if op == '+':
                    reverseMap['root'] -= a
                elif op == '-':
                    reverseMap['root'] = -(reverseMap['root'] - a)
                elif op == '*':
                    reverseMap['root'] //= a
                elif op == '/':
                    reverseMap['root'] = a // reverseMap['root']
                elif op == '==':
                    reverseMap['root'] = a

                return solve(monkey.b)

            except TypeError:
                pass

            # Else solve right half of function
            b = monkey.b.func()
            reverseMap[monkey.b.name] = b

            # Right side reverse
            if op == '+':
                reverseMap['root'] -= b
            elif op == '-':
                reverseMap['root'] += b
            elif op == '*':
                reverseMap['root'] //= b
            elif op == '/':
                reverseMap['root'] *= b
            elif op == '==':
                reverseMap['root'] = b

            return solve(monkey.a)

        # Update root and human functions
        a, _, b = Monkey.monkeys['root'].op.strip().split()
        Monkey.monkeys['root'].op = f'{a} == {b}'
        Monkey.monkeys['root'].func = lambda a=a, b=b: a == b

        Monkey.monkeys['humn'].func = None

        return solve(Monkey.monkeys['root'])


AdventOfCodeBase.run(Day21, 'input.txt')
