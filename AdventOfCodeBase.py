def readLines(file, classType=None):
    classType = int if classType is None else classType
    with open(file, 'r') as myFile:
        result = []
        for line in myFile.readlines():
            result.append(classType(line))
        return result


def readCSV(file, classType=None, delimiter=None):
    classType = int if classType is None else classType
    delimiter = ',' if delimiter is None else delimiter
    with open(file, 'r') as myFile:
        result = []
        for line in myFile.read().split(delimiter):
            result.append(classType(line))
        return result


class AoCProblem:
    def __init__(self, myInput):
        pass

    def readInput(self):
        pass

    def parseInput(self):
        pass

    def p1(self):
        pass

    def p2(self):
        pass
