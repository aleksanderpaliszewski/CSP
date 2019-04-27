import time
import os
from fileReader import fileReader
from futoConstraints import checkCons
from matrices import valuesInMatrix


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
            rec(matrix, valM, cons, 0, col + 1, 0)
    else:
        rec(matrix, valM, cons, row + 1, col, 0)


def rec(matrix, valM, cons, row, col, minus):
    global returns, flag
    height = len(matrix) - 1
    width = len(matrix[0]) - 1
    consItem = checkCons(matrix, cons, row, col)
    consItem = consItem[minus:]

    if flag:
        return
    elif [row, col] in valM:
        skipValue(matrix, valM, cons, row, col, width, height)
    elif int(matrix[row][col]) > 0:
        returns += 1
        return
    elif len(consItem) == 0:
        returns += 1
        return
    elif col == height and row == width:
        returns += 1
        matrix.itemset((row, col), consItem[0])
        flag = True
        return
    elif row == width:
        matrix.itemset((row, col), consItem[0])
        rec(matrix, valM, cons, 0, col + 1, 0)
        matrix.itemset((row, col), 0)
        rec(matrix, valM, cons, row, col, minus + 1)
    else:
        matrix.itemset((row, col), consItem[0])
        rec(matrix, valM, cons, row + 1, col, 0)
        matrix.itemset((row, col), 0)
        rec(matrix, valM, cons, row, col, minus + 1)


def BTStart():
    entries = sorted(os.listdir('./Futoshiki'))
    for entry in entries:
        global returns
        setCounter()
        setFlag()
        matrix, cons = fileReader(entry)
        valuesInMatrix1 = valuesInMatrix(matrix)
        start_time = time.time()
        rec(matrix, valuesInMatrix1, cons, 0, 0, 0)
        print("File = ", entry, " returns = ", str(returns), " Time = %s seconds CSP = FC" % (time.time() - start_time))


if __name__ == '__main__':
    BTStart()
