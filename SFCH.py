import time
import os
import itertools
import numpy as np

from fileReader import fileReaderS
from futoConstraints import checkConsS, checkRegConsS
from matrices import setValues, countValues

flag = False
returns = 0


def setCounter():
    global returns
    returns = 0


def setFlag():
    global flag
    flag = False


def findEmptyH(matrix):
    for i, j in itertools.product(range(len(matrix)), range(len(matrix))):
        if matrix[i][j] == 0:
            if len(checkRegConsS(matrix, i, j)) == 0:
                return True
    return False


def findConCell(matrix, cons):
    x, y = len(matrix) + 1, len(matrix) + 1
    minCons = len(matrix)
    for row, col in itertools.product(range(len(matrix)), range(len(matrix))):
        constraints = len(checkRegConsS(matrix, row, col))
        if minCons > constraints > 0 and matrix[row][col] == 0:
            minCons = constraints
            x = row
            y = col
    return x, y


def itemSet(matrix, cons, row, col, minus, max, consItem, valM):
    matrix.itemset((row, col), consItem)
    newRow, newCol = findConCell(matrix, cons)
    if newRow >= len(matrix):
        matrix.itemset((row, col), 0)
    else:
        recFCH(matrix, valM, cons, newRow, newCol, 0, max)
        matrix.itemset((row, col), 0)
        recFCH(matrix, valM, cons, row, col, minus + 1, max)


def recFCH(matrix, valM, cons, row, col, minus, max):
    global returns, flag
    count = countValues(matrix)
    consItem = checkRegConsS(matrix, row, col)
    consItem = consItem[minus:]

    if flag:
        return
    elif findEmptyH(matrix):
        returns += 1
    elif [row, col] in valM:
        itemSet(matrix, cons, row, col, minus, max, consItem[0], valM)
        returns += 1
    elif len(consItem) == 0:
        returns += 1
    elif count == max - 1:
        matrix.itemset((row, col), consItem[0])
        if checkConsS(matrix, cons):
            flag = True
            returns += 1
            return
        else:
            matrix.itemset((row, col), 0)
            return
    else:
        itemSet(matrix, cons, row, col, minus, max, consItem[0], valM)


def FC():
    entries = sorted(os.listdir('/Users/aleksanderpaliszewski/Desktop/SI/Lab2/Skyscrapper'))
    for entry in entries:
        global returns
        setCounter()
        setFlag()
        cons = fileReaderS(entry)
        matrix = np.zeros((len(cons[0]), len(cons[0])))
        matrix, values = setValues(matrix, cons)
        start_time = time.time()
        recFCH(matrix, values, cons, 0, 0, 0, len(matrix)*len(matrix))
        print("File = ", entry, " returns = ", str(returns), " Time = %s seconds CSP = FC" % (time.time() - start_time))


if __name__ == '__main__':
    FC()
