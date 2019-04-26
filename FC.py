import numpy as np
import time
import os
import itertools

flag = False
returns = 0


def setCounter():
    global returns
    returns = 0


def setFlag():
    global flag
    flag = False


def fileReader(text):
    filename = "./Futoshiki/" + text
    lines, matrix, cons = [], [], []
    with open(filename) as f:
        lines.extend(f.readlines())
    dim = int(lines[0])
    for x in lines[2:dim + 2]:
        matrix.extend(x.replace("\n", "").split(";"))
    for x in lines[dim + 3:len(lines)]:
        cons.extend(x.replace("\n", "").split(";"))
    cons = toLetters(cons)
    matrix = np.reshape(matrix, (dim, dim))
    y = matrix.astype(np.float)
    return y, cons


def regCons(matrix, x, y):
    capabilities = list(range(1, len(matrix) + 1))
    for cell in matrix[x]:
        if int(cell) > 0 and (int(cell) in capabilities):
            capabilities.remove(int(cell))
    for cell in matrix:
        if int(cell[y]) > 0 and (int(cell[y]) in capabilities):
            capabilities.remove(int(cell[y]))
    return capabilities


def connCons(cons, x, y):
    newCons = []
    for element in cons:
        if element[0] == str(x) + str(y) or element[1] == str(x) + str(y):
            newCons.extend([element[0], element[1]])
    return newCons


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


def fileCons(matrix, cons, valList, x, y):
    for element in range(0, len(cons)):
        if cons[element] == str(x) + str(y):
            if element % 2 == 0:
                conX = cons[element + 1][0]
                conY = cons[element + 1][1]
                secondValue = int(matrix[int(conX)][int(conY)])
                if secondValue > 0:
                    valList = takeSmaller(valList, secondValue)
            else:
                conX = cons[element - 1][0]
                conY = cons[element - 1][1]
                secondValue = int(matrix[int(conX)][int(conY)])
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


def toLetters(valList):
    for char in valList:
        if len(char)>0 and char[0].isalpha():
            valList[valList.index(char)] = str(ord(char[0]) - 65) + str(int(char[1]) - 1)
    return valList


def checkCons(matrix, cons, row, col):
    valList = regCons(matrix, row, col)
    conCons = connCons(np.reshape(cons, (int(len(cons) / 2), 2)), row, col)
    consItem = fileCons(matrix, conCons, valList, row, col)
    return consItem


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


def recFC(matrix, valM, cons, row, col, minus):
    global returns, flag
    height = len(matrix) - 1
    width = len(matrix[0]) - 1
    consItem = checkCons(matrix, cons, row, col)
    consItem = consItem[minus:]

    if returns % 20000 == 0:
        print(returns)

    if flag:
        return
    elif findEmpty(matrix, cons, row, col):
        returns += 1
        return
    elif [row, col] in valM:
        returns += 1
        if row == width:
            if col == height:
                print(matrix)
            else:
                recFC(matrix, valM, cons, 0, col + 1, 0)
        else:
            recFC(matrix, valM, cons, row + 1, col, 0)
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
    entries = sorted(os.listdir('./Futoshiki'))
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
