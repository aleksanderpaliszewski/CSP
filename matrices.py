import itertools
from futoConstraints import checkCons, regConsS


def valuesInMatrix(matrix):
    values = []
    for x, y in itertools.product(range(len(matrix)), range(len(matrix))):
        if matrix[x][y] > 0:
            values.append([x, y])
    return values


def countValues(matrix):
    values = 0
    for x, y in itertools.product(range(len(matrix)), range(len(matrix))):
        if matrix[x][y] > 0:
            values += 1
    return values


def findConCell(matrix, cons):
    x, y = len(matrix) + 1, len(matrix) + 1
    minCons = len(matrix)
    for row, col in itertools.product(range(len(matrix)), range(len(matrix))):
        constraints = len(checkCons(matrix, cons, row, col))
        if minCons > constraints > 0 and matrix[row][col] == 0:
            minCons = constraints
            x = row
            y = col
    return x, y


def findEmpty(matrix, cons, x, y):
    for i, j in itertools.product(range(x, len(matrix)), range(y, len(matrix))):
        if matrix[i][j] != 0:
            pass
        else:
            if len(checkCons(matrix, cons, i, j)) == 0:
                return True
    return False


def findEmptyH(matrix, cons):
    for i, j in itertools.product(range(len(matrix)), range(len(matrix))):
        if matrix[i][j] != 0:
            pass
        else:
            if len(checkCons(matrix, cons, i, j)) == 0:
                return True
    return False


def setValues(matrix, cons):
    values = []
    newMatrix = matrix
    for element in range(len(cons[0])):
        if int(cons[0][element]) == len(cons[0]):
            newMatrix[0][element] = 1
            if [0, element] not in values:
                values.append([0, element])
        if int(cons[0][element]) == 1:
            newMatrix[0][element] = len(cons[0])
            if [0, element] not in values:
                values.append([0, element])

    #print(values, "Top")

    for element in range(len(cons[1])):
        if int(cons[1][element]) == len(cons[0]):
            newMatrix[len(matrix)-1][element] = 1
            if [len(matrix)-1, element] not in values:
                values.append([len(matrix)-1, element])
        if int(cons[1][element]) == 1:
            newMatrix[len(matrix)-1][element] = len(cons[0])
            if [len(matrix)-1, element] not in values:
                values.append([len(matrix)-1, element])

    #print(values, "Bottom")


    for element in range(len(cons[2])):
        if int(cons[2][element]) == len(cons[0]):
            newMatrix[element][0] = 1
            if [element, 0] not in values:
                values.append([element, 0])
        if int(cons[2][element]) == 1:
            newMatrix[element][0] = len(cons[0])
            if [element, 0] not in values:
                values.append([element, 0])

    #print(values, "Lewo")


    for element in range(len(cons[3])):
        if int(cons[3][element]) == len(cons[0]):
            newMatrix[element][len(matrix)-1] = 1
            if [element, len(matrix)-1] not in values:
                values.append([element, len(matrix)-1])
        if int(cons[3][element]) == 1:
            newMatrix[element][len(matrix)-1] = len(cons[0])
            if [element, len(matrix)-1] not in values:
                values.append([element, len(matrix)-1])

    #print(values, "Prawo")

    return newMatrix, values


def findEmptyS(matrix):
    for i, j in itertools.product(range(len(matrix)), range(len(matrix))):
        if matrix[i][j] == 0:
            if len(regConsS(matrix, i, j)) == 0:
                return True
    return False
