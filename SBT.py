import time
import os

import numpy as np

from fileReader import fileReaderS
from futoConstraints import regConsS, checkConsInCol, checkConsInRow, checkConsS
from matrices import findEmptyS, setValues

flag = False
returns = 0


def setCounter():
    global returns
    returns = 0


def setFlag():
    global flag
    flag = False


def recFC(matrix, valM, cons, row, col, minus):
    global returns, flag
    height = len(matrix) - 1
    width = len(matrix[0]) - 1
    consItem = regConsS(matrix, row, col)
    consItem = consItem[minus:]

    if flag:
        return
    elif findEmptyS(matrix):
        returns += 1
        return
    elif [row, col] in valM:
        returns += 1
        if row == width:
            if col == height:
                pass
            else:
                recFC(matrix, valM, cons, 0, col + 1, 0)
        else:
            recFC(matrix, valM, cons, row + 1, col, 0)
    elif len(consItem) == 0:
        returns += 1
        return
    elif col == height and row == width:
        matrix.itemset((row, col), consItem[0])
        if checkConsS(matrix, cons):
            flag = True
            returns += 1
            return
        else:
            matrix.itemset((row, col), 0)
            return
    elif row == width:
        matrix.itemset((row, col), consItem[0])
        if checkConsInCol(matrix, cons, row, col):
            returns += 1
            matrix.itemset((row, col), 0)
            recFC(matrix, valM, cons, row, col, minus + 1)
            return
        else:
            recFC(matrix, valM, cons, 0, col + 1, 0)
            matrix.itemset((row, col), 0)
            recFC(matrix, valM, cons, row, col, minus + 1)
    elif col == height:
        matrix.itemset((row, col), consItem[0])
        if checkConsInRow(matrix, cons, row, col):
            returns += 1
            matrix.itemset((row, col), 0)
            recFC(matrix, valM, cons, row, col, minus + 1)
            return
        else:
            recFC(matrix, valM, cons, row + 1, col, 0)
            matrix.itemset((row, col), 0)
            recFC(matrix, valM, cons, row, col, minus + 1)
    else:
        matrix.itemset((row, col), consItem[0])
        recFC(matrix, valM, cons, row + 1, col, 0)
        #print(matrix)
        matrix.itemset((row, col), 0)
        recFC(matrix, valM, cons, row, col, minus + 1)


def BT():
    entries = sorted(os.listdir('/Users/aleksanderpaliszewski/Desktop/SI/Lab2/Skyscrapper'))
    for entry in entries:
        global second
        setCounter()
        setFlag()
        cons = fileReaderS(entry)
        matrix = np.zeros((len(cons[0]), len(cons[0])))
        matrix, values = setValues(matrix, cons)
        start_time = time.time()
        recFC(matrix, values, cons, 0, 0, 0)
        print("File = ", entry, " returns = ", str(returns), " Time = %s seconds CSP = FC" % (time.time() - start_time))


if __name__ == '__main__':
    BT()
