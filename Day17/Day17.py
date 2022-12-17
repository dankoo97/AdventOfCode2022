import AdventOfCodeBase


class Day17(AdventOfCodeBase.AoCProblem):
    rocks = [
        {(x, 0) for x in range(4)},
        {(1, 1), (1, 0), (0, 1), (1, 2), (2, 1)},
        {(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)},
        {(0, x) for x in range(4)},
        {(x // 2, x % 2) for x in range(4)}
    ]

    def readInput(self, myInput):
        result = []
        with open(myInput, 'r') as myFile:
            for line in myFile.read().rstrip().split('\n'):
                result.append(line)
        return result[0]

    def p1(self):
        top = 0
        settled = {(x, -1) for x in range(7)}
        steps = 0
        for i in range(2022):
            rock = {(x+2, y+top+3) for x, y in Day17.rocks[i % 5]}

            # for y in range(top + 7, -2, -1):
            #     print()
            #     for x in range(7):
            #         if (x, y) in rock:
            #             print('@', end='')
            #         elif (x, y) in settled:
            #             print('#', end='')
            #         else:
            #             print('.', end='')
            # print('\n\n\n\n')

            while True:
                if self.values[steps % len(self.values)] == '>':
                    # print('right')
                    nextPos = {(x+1, y) for x, y in rock}
                else:
                    # print('left')
                    nextPos = {(x-1, y) for x, y in rock}
                steps += 1
                if all((0 <= x < 7 for x, y in nextPos)) and nextPos & settled == set():
                    rock = nextPos

                # for y in range(top+7, -2, -1):
                #     print()
                #     for x in range(7):
                #         if (x, y) in rock:
                #             print('@', end='')
                #         elif (x, y) in settled:
                #             print('#', end='')
                #         else:
                #             print('.', end='')
                # print('\n\n\n\n')

                nextPos = {(x, y-1) for x, y in rock}
                # print('fall')
                if nextPos & settled:
                    break
                else:
                    rock = nextPos

                # for y in range(top+7, -2, -1):
                #     print()
                #     for x in range(7):
                #         if (x, y) in rock:
                #             print('@', end='')
                #         elif (x, y) in settled:
                #             print('#', end='')
                #         else:
                #             print('.', end='')
                # print('\n\n\n\n')

            settled |= rock
            top = max(max(y+1 for x, y in rock), top)

        return top

    def p2(self):
        top = 0
        settled = {(x, -1) for x in range(7)}
        steps = 0

        # 10091 ... looks like a number used for modulo, pattern probably starts repeating  somewhere
        print(len(self.values))

        # Assume that first rocks are not part of pattern, but set it up later
        # Arbitrarily picked start of pattern is 941 (Ctrl + F random few lines of visual somewhere in middle),
        # repeats every 1715 == (7 ** 3) * 5 rocks
        #
        # Pattern has a repeating top of 2574 * n + 1440 starting at 941
        #
        # Ergo, ((1000000000000 - 941) // 1715) * 2574 + func(941 + ((1000000000000 - 941) % 1715))
        for i in range(941 + ((1000000000000 - 941) % 1715)):

            if (top % 2574) == 1440:
                print(i)
                print(steps)
                print(top)
                print()
                # for y in range(top+7, -2, -1):
                #     print()
                #     for x in range(7):
                #         if (x, y) in rock:
                #             print('@', end='')
                #         elif (x, y) in settled:
                #             print('#', end='')
                #         else:
                #             print('.', end='')
                # print('\n\n\n\n')

            rock = {(x + 2, y + top + 3) for x, y in Day17.rocks[i % 5]}

            # for y in range(top + 7, -2, -1):
            #     print()
            #     for x in range(7):
            #         if (x, y) in rock:
            #             print('@', end='')
            #         elif (x, y) in settled:
            #             print('#', end='')
            #         else:
            #             print('.', end='')
            # print('\n\n\n\n')

            while True:

                if steps == 0:
                    print(i)

                if self.values[steps % len(self.values)] == '>':
                    # print('right')
                    nextPos = {(x + 1, y) for x, y in rock}
                else:
                    # print('left')
                    nextPos = {(x - 1, y) for x, y in rock}
                steps += 1
                if all((0 <= x < 7 for x, y in nextPos)) and nextPos & settled == set():
                    rock = nextPos

                # for y in range(top+7, -2, -1):
                #     print()
                #     for x in range(7):
                #         if (x, y) in rock:
                #             print('@', end='')
                #         elif (x, y) in settled:
                #             print('#', end='')
                #         else:
                #             print('.', end='')
                # print('\n\n\n\n')

                nextPos = {(x, y - 1) for x, y in rock}
                # print('fall')
                if nextPos & settled:
                    break
                else:
                    rock = nextPos

                # for y in range(top+7, -2, -1):
                #     print()
                #     for x in range(7):
                #         if (x, y) in rock:
                #             print('@', end='')
                #         elif (x, y) in settled:
                #             print('#', end='')
                #         else:
                #             print('.', end='')
                # print('\n\n\n\n')

            settled |= rock
            top = max(max(y + 1 for x, y in rock), top)

        # for y in range(top+7, -2, -1):
        #     print()
        #     for x in range(7):
        #         if (x, y) in rock:
        #             print('@', end='')
        #         elif (x, y) in settled:
        #             print('#', end='')
        #         else:
        #             print('.', end='')
        # print('\n\n\n\n')
        return top + ((1000000000000 - 941) // 1715) * 2574


AdventOfCodeBase.run(Day17, 'input.txt')
