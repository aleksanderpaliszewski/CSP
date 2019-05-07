import itertools
from Futoshiki.futoConstraints import checkCons


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
