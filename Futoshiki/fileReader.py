import numpy as np


def fileReader(text):
    filename = "./Futoshiki//FutoshikiTestFiles/" + text
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
    y = matrix.astype(np.int)
    return y, cons


def toLetters(valList):
    for char in valList:
        if len(char) > 0 and char[0].isalpha():
            valList[valList.index(char)] = str(ord(char[0]) - 65) + str(int(char[1]) - 1)
    return valList
