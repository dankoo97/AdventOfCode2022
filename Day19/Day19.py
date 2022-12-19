import re

import AdventOfCodeBase


def nextCycle(items, bots, bp, bought=None):
    if bought is None:
        return tuple(i + b for i, b in zip(items, bots)), bots
    else:
        return tuple(i + b - c for i, b, c in zip(items, bots, bp[bought])), tuple(b + (i == bought) for i, b in enumerate(bots))


def canBuy(items, bp, bot):
    return all(items[i] >= bp[bot][i] for i in range(4))


class Day19(AdventOfCodeBase.AoCProblem):
    def readInput(self, myInput):
        result = []
        with open(myInput, 'r') as myFile:
            for bp in myFile.read().rstrip().split('\n'):
                ore = re.findall(r'ore robot costs (\d+) ore', bp)
                clay = re.findall(r'clay robot costs (\d+) ore', bp)
                obsidian = re.findall(r'obsidian robot costs (\d+) ore and (\d+) clay', bp)[0]
                geode = re.findall(r'geode robot costs (\d+) ore and (\d+) obsidian', bp)[0]
                result.append([
                    (int(ore[0]), 0, 0, 0),
                    (int(clay[0]), 0, 0, 0),
                    (int(obsidian[0]), int(obsidian[1]), 0, 0),
                    (int(geode[0]), 0, int(geode[1]), 0),
                ])

        return result

    def p1(self):
        quality = 0
        maxMinutes = 24
        for i, bp in enumerate(self.values[:], 1):
            path = {}
            bots = (1, 0, 0, 0)
            items = (0, 0, 0, 0)
            minutes = 0
            maxGeodes = -1
            maxPath = None

            # Don't build more bots than any other bot might need its materials
            # Example: If all the bots require at most 4 ores, we don't need to build more than 4 ore-producing bots
            maxOut = [0 for _ in range(4)]
            for item in bp:
                for j, a in enumerate(maxOut):
                    maxOut[j] = max(a, item[j])

            # print(maxOut)

            # DFS
            fringe = [(items, bots, minutes, b) for b in (0, 1)]

            while fringe:
                items, bots, minutes, nextBot = fringe.pop(-1)
                remaining = maxMinutes - minutes

                if minutes == maxMinutes:
                    if items[3] > maxGeodes:
                        # print(items, bots, minutes)
                        maxGeodes = items[3]
                        maxPath = items, bots, minutes, nextBot
                    continue
                # Current amount + current rate + max potential rate
                # If I can build 1 geode bot each turn and not reach the max then prune the tree
                elif items[3] + remaining * bots[3] + ((remaining * remaining + remaining) >> 1) <= maxGeodes:
                    continue

                if canBuy(items, bp, nextBot):
                    nextItems, nextBots = nextCycle(items, bots, bp, nextBot)
                    for newBot in range(4):
                        # Branch into potential new bots
                        # Skip bots that could never be built next or bots that do not need to produce faster
                        if (bots[newBot - 1] > 0 or newBot == 0) and (maxOut[newBot] > bots[newBot] or newBot == 3):
                            node = (nextItems, nextBots, minutes+1, newBot)
                            fringe.append(node)
                            path[node] = items, bots, minutes, nextBot
                else:
                    nextItems, nextBots = nextCycle(items, bots, bp)
                    node = (nextItems, nextBots, minutes+1, nextBot)
                    fringe.append(node)
                    path[node] = items, bots, minutes, nextBot

            # Reproduce the best path
            # stack = []
            # curr = maxPath
            # while curr in path:
            #     stack.insert(0, curr)
            #     curr = path[curr]
            #
            # for items, bots, minute, _ in stack:
            #     print(f'Minute {minute}\nItems: {items}\nBots: {bots}\n\n')
            #
            # print(i, maxGeodes)

            quality += maxGeodes * i
        return quality

    def p2(self):
        # Same as p1 with modifications for time and final result calculation

        quality = 1
        maxMinutes = 32
        for bp in self.values[:3]:
            path = {}
            bots = (1, 0, 0, 0)
            items = (0, 0, 0, 0)
            minutes = 0
            maxGeodes = -1
            maxPath = None
            maxOut = [0 for _ in range(4)]
            for item in bp:
                for j, a in enumerate(maxOut):
                    maxOut[j] = max(a, item[j])

            # print(maxOut)

            fringe = [(items, bots, minutes, b) for b in (0, 1)]

            while fringe:
                items, bots, minutes, nextBot = fringe.pop(-1)
                remaining = maxMinutes - minutes

                if minutes == maxMinutes:
                    if items[3] > maxGeodes:
                        # print(items, bots, minutes)
                        maxGeodes = items[3]
                        maxPath = items, bots, minutes, nextBot
                    continue
                # Current amount + current rate + max potential rate
                elif items[3] + remaining * bots[3] + (
                        (remaining * remaining + remaining) >> 1) <= maxGeodes:  # If I can build 1 geode bot each turn
                    continue

                if canBuy(items, bp, nextBot):
                    nextItems, nextBots = nextCycle(items, bots, bp, nextBot)
                    for newBot in range(4):
                        if (bots[newBot - 1] > 0 or newBot == 0) and (maxOut[newBot] > bots[newBot] or newBot == 3):
                            node = (nextItems, nextBots, minutes + 1, newBot)
                            fringe.append(node)
                            path[node] = items, bots, minutes, nextBot

                else:
                    nextItems, nextBots = nextCycle(items, bots, bp)
                    node = (nextItems, nextBots, minutes + 1, nextBot)
                    fringe.append(node)
                    path[node] = items, bots, minutes, nextBot

            # stack = []
            # curr = maxPath
            # while curr in path:
            #     stack.insert(0, curr)
            #     curr = path[curr]
            #
            # for items, bots, minute, _ in stack:
            #     print(f'Minute {minute}\nItems: {items}\nBots: {bots}\n\n')
            #
            # print(maxGeodes)

            quality *= maxGeodes
        return quality


AdventOfCodeBase.run(Day19, 'input.txt')
