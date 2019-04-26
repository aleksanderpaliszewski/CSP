import numpy as np
import time
import os
import itertools


futoshiki = []
first = 0
second = 0
third = 0
loadTime = 0
loadTime2 = 0
flaga = False
flaga2 = False


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
    # print(len(cons))
    cons = toLetters(cons)
    return np.reshape(matrix, (dim, dim)), cons


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


def fileConsPrint(matrix, cons, valList, x, y):
    for element in range(0, len(cons)):
        if cons[element] == str(x) + str(y):
            if element % 2 == 0:
                conX = cons[element + 1][0]
                conY = cons[element + 1][1]
                secondValue = int(matrix[int(conX)][int(conY)])
                if secondValue > 0:
                    valList = takeSmaller(valList, secondValue)
                    print("Take smaller = ", valList, " conX = ", conX, "conY = ", conY, " Second Value = ",
                          secondValue, " Element = ", element)
            else:
                conX2 = cons[element][0]
                conY2 = cons[element][1]
                secondValue = int(matrix[int(conX2)][int(conY2)])
                if secondValue > 0:
                    valList = takeBigger(valList, secondValue)
                    print("Take biggger = ", valList, " conX = ", conX2, "conY = ", conY2, " Second Value = ",
                          secondValue, " Element = ", element)
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


# OPTYMALIZACJA!

def findEmpty(matrix, cons, x, y):
    for i, j in itertools.product(range(x, len(matrix)), range(y, len(matrix))):
        if int(matrix[i][j]) != 0:
            return
        else:
            constraints = len(checkCons(matrix, cons, i, j))
            if constraints == 0:
                return True
    return False


def findEmpty2(matrix, cons):
    for i, j in itertools.product(range(len(matrix)), range(len(matrix))):
        if int(matrix[i][j]) != 0:
            pass
        else:
            constraints = len(checkCons(matrix, cons, i, j))
            if constraints == 0:
                return True
    return False


def rec(matrix, valM, cons, row, col, minus):
    global first, flaga2
    height = len(matrix) - 1
    width = len(matrix[0]) - 1
    consItem = checkCons(matrix, cons, row, col)
    consItem = consItem[minus:]

    if flaga2:
        return
    elif [row, col] in valM:
        first += 1
        if row == width:
            if col == height:
                print(matrix)
            else:
                rec(matrix, valM, cons, 0, col + 1, 0)
        else:
            rec(matrix, valM, cons, row + 1, col, 0)
    elif int(matrix[row][col]) > 0:
        first += 1
        return
    elif len(consItem) == 0:
        first += 1
        return
    elif col == height and row == width:
        first += 1
        matrix.itemset((row, col), consItem[0])
        flaga2 = True
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


def recFC(matrix, valM, cons, row, col, minus):
    global second, loadTime, flaga
    height = len(matrix) - 1
    width = len(matrix[0]) - 1
    consItem = checkCons(matrix, cons, row, col)
    consItem = consItem[minus:]
    if flaga:
        return
    elif findEmpty(matrix, cons, row, col):
        second += 1
        return
    elif [row, col] in valM:
        second += 1
        if row == width:
            if col == height:
                print(matrix)
            else:
                recFC(matrix, valM, cons, 0, col + 1, 0)
        else:
            recFC(matrix, valM, cons, row + 1, col, 0)
    elif len(consItem) == 0:
        second += 1
        return
    elif col == height and row == width:
        matrix.itemset((row, col), consItem[0])
        flaga = True
        second += 1
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


def rec2(matrix, valM, cons, row, col, minus, max):
    global first, flaga
    count = countValues(matrix)
    consItem = checkCons(matrix, cons, row, col)
    consItem = consItem[minus:]

    if flaga:
        return
    elif len(consItem) == 0:
        first += 1
        return
    elif count == max - 1:
        matrix.itemset((row, col), consItem[0])
        flaga = True
        return
    else:
        matrix.itemset((row, col), consItem[0])
        newRow, newCol = findConCell(matrix, cons)
        if newRow >= len(matrix):
            matrix.itemset((row, col), 0)
            return
        elif len(checkCons(matrix, cons, newRow, newCol)) == 0:
            matrix.itemset((row, col), 0)
            return
        else:
            rec2(matrix, valM, cons, newRow, newCol, 0, max)
            matrix.itemset((row, col), 0)
            rec2(matrix, valM, cons, row, col, minus + 1, max)


def rec3(matrix, valM, cons, row, col, minus, max):
    global second, flaga2
    count = countValues(matrix)
    consItem = checkCons(matrix, cons, row, col)
    consItem = consItem[minus:]

    if flaga2:
        return
    elif findEmpty2(matrix, cons):
        second += 1
        return
    elif len(consItem) == 0:
        second += 1
        return
    elif count == max - 1:
        matrix.itemset((row, col), consItem[0])
        flaga2 = True
        return
    else:
        matrix.itemset((row, col), consItem[0])
        newRow, newCol = findConCell(matrix, cons)
        if newRow >= len(matrix):
            matrix.itemset((row, col), 0)
            return
        else:
            rec3(matrix, valM, cons, newRow, newCol, 0, max)
            matrix.itemset((row, col), 0)
            rec3(matrix, valM, cons, row, col, minus + 1, max)


def setGlobar():
    global loadTime
    loadTime = 0


def setFirst():
    global first
    first = 0


def setSecond():
    global second
    second = 0

def setFlag():
    global flaga
    flaga = False


def setFlag2():
    global flaga2
    flaga2 = False


def BT():
    entries = sorted(os.listdir('./Futoshiki'))
    for entry in entries:
        global second
        setGlobar()
        setFirst()
        setFlag()
        matrix, cons = fileReader(entry)
        valuesInMatrix1 = valuesInMatrix(matrix)
        start_time = time.time()
        print()
        rec2(matrix, valuesInMatrix1, cons, 0, 0, 0, len(matrix)*len(matrix))
        print("File = ", entry, " returns = ", str(first), " Time = %s seconds CSP = BT" % (time.time() - start_time))


def FC():
    entries = sorted(os.listdir('./Futoshiki'))
    for entry in entries:
        global second
        print()
        setGlobar()
        setSecond()
        setFlag2()
        matrix, cons = fileReader(entry)
        valuesInMatrix1 = valuesInMatrix(matrix)
        start_time = time.time()
        rec3(matrix, valuesInMatrix1, cons, 0, 0, 0, len(matrix)*len(matrix))
        print("File = ", entry, " returns = ", str(second), " Time = %s seconds CSP = FC" % (time.time() - start_time))


if __name__ == '__main__':
    FC()
    BT()
