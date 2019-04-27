import time
import os
import itertools
from fileReader import fileReader
from futoConstraints import checkCons


flag = False
returns = 0


def setCounter():
    global returns
    returns = 0


def setFlag():
    global flag
    flag = False


def valuesInMatrix(matrix):
    values = []
    for x, y in itertools.product(range(len(matrix)), range(len(matrix))):
        if int(matrix[x][y]) > 0:
            values.append([x, y])
    return values


def countValues(matrix):
    values = 0
    for x, y in itertools.product(range(len(matrix)), range(len(matrix))):
        if int(matrix[x][y]) > 0:
            values += 1
    return values


def findConCell(matrix, cons):
    x, y = len(matrix) + 1, len(matrix) + 1
    minCons = len(matrix)
    for row, col in itertools.product(range(len(matrix)), range(len(matrix))):
        constraints = len(checkCons(matrix, cons, row, col))
        if minCons > constraints > 0 and int(matrix[row][col]) == 0:
            minCons = constraints
            x = row
            y = col
    return x, y


def findEmpty(matrix, cons, x, y):
    for i, j in itertools.product(range(x, len(matrix)), range(y, len(matrix))):
        if int(matrix[i][j]) != 0:
            return
        else:
            constraints = len(checkCons(matrix, cons, i, j))
            if constraints == 0:
                return True
    return False


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
    entries = sorted(os.listdir('./Futoshiki'))
    for entry in entries:
        global returns
        setCounter()
        setFlag()
        matrix, cons = fileReader(entry)
        valuesInMatrix1 = valuesInMatrix(matrix)
        start_time = time.time()
        recBTH(matrix, cons, 0, 0, 0, len(matrix) * len(matrix))
        print("File = ", entry, " returns = ", str(returns), " Time = %s seconds CSP = FC" % (time.time() - start_time))


if __name__ == '__main__':
    BTStart()
