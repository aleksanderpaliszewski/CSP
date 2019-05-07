import time
import os
from Futoshiki.fileReader import fileReader
from Futoshiki.futoConstraints import checkCons
from matrices import findConCell, countValues


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
        recBTH(matrix, cons, newRow, newCol, 0, max)
        matrix.itemset((row, col), 0)
        recBTH(matrix, cons, row, col, minus + 1, max)


def recBTH(matrix, cons, row, col, minus, max):
    global returns, flag
    count = countValues(matrix)
    consItem = checkCons(matrix, cons, row, col)
    consItem = consItem[minus:]

    # if returns%10000 == 0:
    #     print(returns)

    if flag:
        return
    elif len(consItem) == 0:
        returns += 1
        return
    elif count == max - 1:
        matrix.itemset((row, col), consItem[0])
        flag = True
        return
    else:
        itemSet(matrix, cons, row, col, minus, max, consItem[0])


def BTStart():
    entries = sorted(os.listdir('./FutoshikiTestFiles'))
    for entry in entries:
        global returns
        setCounter()
        setFlag()
        matrix, cons = fileReader(entry)
        start_time = time.time()
        recBTH(matrix, cons, 0, 0, 0, len(matrix) * len(matrix))
        print("File = ", entry, " returns = ", str(returns), " Time = %s seconds CSP = FC" % (time.time() - start_time))


if __name__ == '__main__':
    BTStart()
