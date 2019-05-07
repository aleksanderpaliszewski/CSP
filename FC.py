import time
import os
from fileReader import fileReader
from futoConstraints import checkCons
from matrices import valuesInMatrix, findEmpty

flag = False
returns = 0


def setCounter():
    global returns
    returns = 0


def setFlag():
    global flag
    flag = False


def skipValue(matrix, valM, cons, row, col, width, height):
    if row == width:
        if col == height:
            print(matrix)
        else:
            recFC(matrix, valM, cons, 0, col + 1, 0)
    else:
        recFC(matrix, valM, cons, row + 1, col, 0)


def recFC(matrix, valM, cons, row, col, minus):
    global returns, flag
    height = len(matrix) - 1
    width = len(matrix[0]) - 1
    consItem = checkCons(matrix, cons, row, col)
    consItem = consItem[minus:]

    # if returns % 20000 == 0 and returns != 0:
    #     print(returns)

    if flag:
        return
    elif findEmpty(matrix, cons, row, col):
        returns += 1
        return
    elif [row, col] in valM:
        returns += 1
        skipValue(matrix, valM, cons, row, col, width, height)
    elif len(consItem) == 0:
        returns += 1
        return
    elif col == height and row == width:
        matrix.itemset((row, col), consItem[0])
        flag = True
        returns += 1
        return
    elif row == width:
        matrix.itemset((row, col), consItem[0])
        recFC(matrix, valM, cons, 0, col + 1, 0)
        matrix.itemset((row, col), 0)
        recFC(matrix, valM, cons, row, col, minus + 1)
    else:
        matrix.itemset((row, col), consItem[0])
        recFC(matrix, valM, cons, row + 1, col, 0)
        matrix.itemset((row, col), 0)
        recFC(matrix, valM, cons, row, col, minus + 1)


def FCStart():
    entries = sorted(os.listdir('./FutoshikiTestFiles'))
    for entry in entries:
        global returns
        setCounter()
        setFlag()
        matrix, cons = fileReader(entry)
        valuesInMatrix1 = valuesInMatrix(matrix)
        start_time = time.time()
        recFC(matrix, valuesInMatrix1, cons, 0, 0, 0)
        print("File = ", entry, " returns = ", str(returns), " Time = %s seconds CSP = FC" % (time.time() - start_time))


if __name__ == '__main__':
    FCStart()
