from random import randint
from copy import deepcopy

def findEmptyLocations(sudoko, coords):
    for rowIdx in range(9):
        for columnIdx in range(9):
            if sudoko[rowIdx][columnIdx] == 0:
                coords[0], coords[1] = rowIdx, columnIdx
                return True         
    return False

def checkColumns(row, column, num, sudoko):
    for r in range(9):
        if sudoko[r][column] == num and r != row:
            return False
    return True

def checkRows(row, column, num, sudoko):
    for col in range(9):
        if sudoko[row][col] == num and column != col:
            return False
    return True

def checkSector(row, column, num, sudoko):
    startRow = row - (row%3)
    startColumn = column - (column%3)
    for offsetRow in range(3):
        for offsetColumn in range(3):
            if sudoko[startRow + offsetRow][startColumn + offsetColumn] == num and startRow + offsetRow != row and startColumn + offsetColumn != column:
                return False
    return True

def checkIfSafe(row, column, num, sudoko):
    if checkSector(row, column, num, sudoko) and checkRows(row, column, num,sudoko) and checkColumns(row, column, num, sudoko):
        return True
    return False

def solveSudoko(sudoko):
    coords = [0, 0]

    if not findEmptyLocations(sudoko, coords):
        return True
    
    rowIdx, columnIdx = coords[0], coords[1]
    for num in range(1, 10):
        if checkIfSafe(rowIdx, columnIdx, num, sudoko):
            sudoko[rowIdx][columnIdx] = num     
            if solveSudoko(sudoko):
                return sudoko                   
            sudoko[rowIdx][columnIdx] = 0
    return False

def findSudoko():
    sudokoNo, found = randint(1, 50), False
    with open('sudokoGrids.txt','r') as f:
        for i in range(50):
            sudoko = []
            for j in range(10):
                if j != 0 and i+1 == sudokoNo:
                    row = f.readline().strip()
                    line = [int(digit) for digit in row]
                    sudoko.append(line)
                    found = True   
                else:
                    row = f.readline().strip()

            if found:
                return sudoko

def main():
    Grid = findSudoko()
    unsolvedGrid = deepcopy(Grid)
    UserGrid = deepcopy(Grid)

    solvedGrid = solveSudoko(Grid)
    return unsolvedGrid, UserGrid, solvedGrid

if __name__ == '__main__':
    main()
