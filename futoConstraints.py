import numpy as np


def checkCons(matrix, cons, row, col):
    valList = regCons(matrix, row, col)
    conCons = connCons(np.reshape(cons, (int(len(cons) / 2), 2)), row, col)
    consItem = fileCons(matrix, conCons, valList, row, col)
    return consItem


def checkRegConsS(matrix, row, col):
    valList = regCons(matrix, row, col)
    return valList


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


def regConsS(matrix, x, y):
    capabilities = list(range(1, len(matrix) + 1))
    for cell in matrix[x]:
        if cell > 0 and cell in capabilities:
            capabilities.remove(int(cell))
    for cell in matrix:
        if cell[y] > 0 and cell[y] in capabilities:
            capabilities.remove(int(cell[y]))
    return capabilities


def checkConsS(matrix, cons):
    for row in range(0, len(matrix)):
        left, right, top, bottom = 1, 1, 1, 1
        valueLeft = matrix[row][0]
        valueRight = matrix[row][len(matrix) - 1]
        valueTop = matrix[0][row]
        valueBottom = matrix[len(matrix) - 1][row]

        for element in range(0, len(matrix)):
            if valueLeft < matrix[row][element]:
                valueLeft = matrix[row][element]
                left += 1
        if left != int(cons[2][row]) and int(cons[2][row]) != 0:
            return False

        for element in range(len(matrix) - 1, -1, -1):
            # print(matrix[row][element])
            if valueRight < matrix[row][element]:
                valueRight = matrix[row][element]
                right += 1
        if right != int(cons[3][row]) and int(cons[3][row]) != 0:
            return False

        for element in range(0, len(matrix)):
            if valueTop < matrix[element][row]:
                valueTop = matrix[element][row]
                top += 1
        if top != int(cons[0][row]) and int(cons[0][row]) != 0:
            return False

        for element in range(len(matrix) - 1, -1, -1):
            if valueBottom < matrix[element][row]:
                valueBottom = matrix[element][row]
                bottom += 1
        if bottom != int(cons[1][row]) and int(cons[1][row]) != 0:
            return False
    return True


def checkConsInRow(matrix, cons, x, y):
    left, right, top, bottom = 1, 1, 1, 1
    valueLeft = matrix[x][0]
    valueRight = matrix[x][len(matrix) - 1]

    for element in range(0, x):
        if valueLeft < matrix[x][element]:
            valueLeft = matrix[x][element]
            left += 1
    #print("LEFT Counter = ", left, " cons = ", cons[2][x], " bool = ", left > int(cons[2][x]) > 0)
    if left > int(cons[2][x]) > 0:
        return True

    for element in range(x - 1, -1, -1):
        if valueRight < matrix[x][element]:
            valueRight = matrix[x][element]
            right += 1
    #print("RIGHT Counter = ", right, " cons = ", cons[3][x], " bool = ", right > int(cons[3][x]) > 0)
    if right > int(cons[3][x]) > 0:
        return True
    return False


def checkConsInCol(matrix, cons, x, y):
    left, right, top, bottom = 1, 1, 1, 1
    valueTop = matrix[0][y]
    valueBottom = matrix[len(matrix) - 1][y]

    for element in range(0, y):
        if valueTop < matrix[element][y]:
            valueTop = matrix[element][y]
            top += 1
   # print("TOP Counter = ", top, " cons = ", cons[0][y], " bool = ", top > int(cons[0][y]) > 0)
    if top > int(cons[0][y]) > 0:
        return True

    for element in range(x - 1, -1, -1):
        if valueBottom < matrix[element][y]:
            valueBottom = matrix[element][y]
            bottom += 1
    #print("BOTTOM Counter = ", bottom, " cons = ", cons[1][y], " bool = ", bottom > int(cons[1][y]) > 0)
    if bottom > int(cons[1][y]) > 0:
        return True
    return False