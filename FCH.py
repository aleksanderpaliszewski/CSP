import time
import os
from fileReader import fileReader
from futoConstraints import checkCons
from matrices import findEmptyH, findConCell, countValues

flag = False
returns = 0


def setCounter():
    global returns
    returns = 0


def setFlag():
    global flag
    flag = False


def itemSet(matrix, cons, row, col, minus, max, consItem):
    matrix.itemset((row, col), consItem)
    newRow, newCol = findConCell(matrix, cons)
    if newRow >= len(matrix):
        matrix.itemset((row, col), 0)
    else:
        recFCH(matrix, cons, newRow, newCol, 0, max)
        matrix.itemset((row, col), 0)
        recFCH(matrix, cons, row, col, minus + 1, max)


def recFCH(matrix, cons, row, col, minus, max):
    global returns, flag
    count = countValues(matrix)
    consItem = checkCons(matrix, cons, row, col)
    consItem = consItem[minus:]

    # if returns % 20000 == 0 and returns != 0:
    #     print(returns)

    if flag:
        return
    elif findEmptyH(matrix, cons):
        returns += 1
    elif len(consItem) == 0:
        returns += 1
    elif count == max - 1:
        flag = True
        matrix.itemset((row, col), consItem[0])
    else:
        itemSet(matrix, cons, row, col, minus, max, consItem[0])


def FCStart():
    entries = sorted(os.listdir('./Futoshiki'))
    for entry in entries:
        global returns
        setCounter()
        setFlag()
        matrix, cons = fileReader(entry)
        start_time = time.time()
        recFCH(matrix, cons, 0, 0, 0, len(matrix)*len(matrix))
        print("File = ", entry, " returns = ", str(returns), " Time = %s seconds CSP = FC" % (time.time() - start_time))


if __name__ == '__main__':
    FCStart()
