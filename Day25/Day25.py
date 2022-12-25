import math

import AdventOfCodeBase


def convertFromSNAFU(s):
    x = 0
    for c in s:
        x *= 5
        match c:
            case '2':
                x += 2
            case '1':
                x += 1
            case '0':
                x += 0
            case '-':
                x -= 1
            case '=':
                x -= 2
    return x


def convertToSNAFU(s):
    n = ''
    for i in range(int(math.log(s, 5)) + 1, 0, -1):
        if s > 0:
            fivePow = int(math.pow(5, i))
            if fivePow >> 1 > s:
                n += '0'
            elif (fivePow >> 1) + fivePow > s:
                n += '1'
                s -= fivePow
            else:
                n += '2'
                s -= fivePow << 1
        elif s < 0:
            fivePow = int(math.pow(5, i))
            if fivePow >> 1 > abs(s):
                n += '0'
            elif (fivePow >> 1) + fivePow > abs(s):
                n += '-'
                s += fivePow
            else:
                n += '='
                s += fivePow << 1
        else:
            n += '0'
    else:
        # Logic breaks down at 1s place, easier to implement temp patch and leave it forever
        match s:
            case -2:
                n += '='
            case -1:
                n += '-'
            case 0:
                n += '0'
            case 1:
                n += '1'
            case 2:
                n += '2'
    return n.lstrip('0')


class Day25(AdventOfCodeBase.AoCProblem):
    def readInput(self, myInput):
        result = []
        with open(myInput, 'r') as myFile:
            for line in myFile.read().rstrip().split('\n'):
                result.append(line)

        return result

    def p1(self):
        s = 0
        for line in self.values:
            s += convertFromSNAFU(line)

        n = convertToSNAFU(s)

        assert s == convertFromSNAFU(n)

        return n

    def p2(self):
        return 'Merry Christmas!'


AdventOfCodeBase.run(Day25, 'input.txt')
