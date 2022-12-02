import AdventOfCodeBase


class Day02 (AdventOfCodeBase.AoCProblem):
    def __init__(self, myInput):
        super().__init__(myInput)

    def readInput(self, myInput):
        with open(myInput, 'r') as myFile:
            gameRound = []
            for line in myFile.read().strip().split('\n'):
                gameRound.append(line.split())
        return gameRound

    def parseInput(self, myInput):
        return myInput

    def p1(self):
        score = 0
        points = {
            'X': 1,
            'Y': 2,
            'Z': 3,
        }
        for them, me in self.values:
            score += points[me]
            them = chr(ord(them) + 23)
            if them == me:
                score += 3
            elif chr((ord(them) + 1) % 3 + 88) == me:
                score += 0
            else:
                score += 6
        return score

    def p2(self):
        score = 0
        points = {
            'A': 1,
            'B': 2,
            'C': 3,
            'X': 0,
            'Y': 3,
            'Z': 6,
        }
        for them, me in self.values:
            score += points[me]
            if me == 'X':
                score += points[chr((ord(them)) % 3 + 65)]
            elif me == 'Z':
                score += points[chr((ord(them) - 1) % 3 + 65)]
            else:
                score += points[them]
        return score


AdventOfCodeBase.run(Day02, "input.txt")
