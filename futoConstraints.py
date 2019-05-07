import numpy as np


def checkCons(matrix, cons, row, col):
    valList = regCons(matrix, row, col)
    conCons = connCons(np.reshape(cons, (int(len(cons) / 2), 2)), row, col)
    consItem = fileCons(matrix, conCons, valList, row, col)
    return consItem


def regCons(matrix, x, y):
    capabilities = list(range(1, len(matrix) + 1))
    for cell in matrix[x]:
        if cell > 0 and cell in capabilities:
            capabilities.remove(cell)
    for cell in matrix:
        if cell[y] > 0 and cell[y] in capabilities:
            capabilities.remove(cell[y])
    return capabilities


def connCons(cons, x, y):
    newCons = []
    for element in cons:
        if element[0] == str(x) + str(y) or element[1] == str(x) + str(y):
            newCons.extend([element[0], element[1]])
    return newCons


def fileCons(matrix, cons, valList, x, y):
    for element in range(0, len(cons)):
        if cons[element] == str(x) + str(y):
            if element % 2 == 0:
                conX = int(cons[element + 1][0])
                conY = int(cons[element + 1][1])
                secondValue = matrix[conX][conY]
                if secondValue > 0:
                    valList = takeSmaller(valList, secondValue)
            else:
                conX = int(cons[element - 1][0])
                conY = int(cons[element - 1][1])
                secondValue = matrix[conX][conY]
                if secondValue > 0:
                    valList = takeBigger(valList, secondValue)
    return valList


def takeSmaller(valList, value):
    smallerValues = []
    for element in valList:
        if element < value:
            smallerValues.append(element)
    return smallerValues


def takeBigger(valList, value):
    biggerValues = []
    for element in valList:
        if element > value:
            biggerValues.append(element)
    return biggerValues
