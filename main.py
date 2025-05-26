import sys
import math
import re
from copy import deepcopy

DIRECTIONS = {
    "haut":    {"dx": -1, "dy":  0, "char": "^", "invChar": "v"},
    "bas":     {"dx":  1, "dy":  0, "char": "v", "invChar": "^"},
    "gauche":  {"dx":  0, "dy": -1, "char": "<", "invChar": ">"},
    "droite":  {"dx":  0, "dy":  1, "char": ">", "invChar": "<"},
}

BALL_PATTERN = re.compile(r"[1-9]")

def isWin(ballPos, ballPosIndex):
    return ballPosIndex == len(ballPos) 

def generateResultsDirection(resultArray, board, result, ballPos, ballPosIndex, coupPos, coupIndex, i, direction):
    dx = DIRECTIONS[direction]["dx"]
    dy = DIRECTIONS[direction]["dy"]
    char = DIRECTIONS[direction]["char"]
    invChar = DIRECTIONS[direction]["invChar"]

    valide = True
    resultNew = deepcopy(result)
    ballPosIndexNew = ballPosIndex
    coupIndexNew = coupIndex + 1
    x, y = coupPos
    coupPos_x, couPos_y = coupPos
    ballPos_x, ballPos_y = ballPos[ballPosIndex]
    rows, cols = len(board), len(board[0])
    nbCases = i

    if (direction == "haut" and x == 0) or \
        (direction == "bas" and x == rows - 1) or \
        (direction == "gauche" and y == 0) or \
        (direction == "droite" and y == cols - 1) or \
        (result[x][y] == invChar):
            return

    while 0 <= x < rows and 0 <= y < cols:
        cell_result = result[x][y]
        cell_board = board[x][y]
        
        if nbCases < 0:
            break
        
        if (direction == "haut" and x == 0) or \
        (direction == "bas" and x == rows - 1) or \
        (direction == "gauche" and y == 0) or \
        (direction == "droite" and y == cols - 1):
            if cell_board == "X":
                valide = False
                break

        if x != ballPos_x and y != ballPos_y and '1' <= cell_board <= '9':
            valide = False
            break
        
        if x != coupPos_x and y != couPos_y and cell_result in {"^", "v", "<", ">"}:
            valide = False
            break

        if cell_board == "H":
            occupe = False
            for d in DIRECTIONS.keys():
                around_x = x+DIRECTIONS[d]["dx"]
                around_y = y+DIRECTIONS[d]["dy"]
                if 0 <= around_x < rows and 0 <= around_y < cols and \
                (d != direction and board[around_x][around_y] == DIRECTIONS[d]["invChar"]):
                    occupe = True
            if occupe:
                valide = False
                break
            else:
                ballPosIndexNew = ballPosIndex + 1
                coupIndexNew  = 0
                if ballPosIndexNew < len(ballPos):
                    coupPosNew = ballPos[ballPosIndexNew]
                else:
                    coupPosNew = None
                break

        resultNew[x][y] = char
        coupPosNew = (x,y)
        x += dx
        y += dy
        nbCases -= 1

    if valide:
        resultArray.append((resultNew, ballPosIndexNew, coupPosNew, coupIndexNew))


def generateResultsFromResult(board, result, ballPos, ballPosIndex, coupPos, coupIndex):
    resultArray = []
    ballPos_x, ballPos_y = ballPos[ballPosIndex]
    nbMaxCoup = int(board[ballPos_x][ballPos_y])
    if coupIndex < nbMaxCoup:
        for i in reversed(range(nbMaxCoup - coupIndex)):
            generateResultsDirection(resultArray, board, result, ballPos, ballPosIndex, coupPos, coupIndex, i, "haut")
            generateResultsDirection(resultArray, board, result, ballPos, ballPosIndex, coupPos, coupIndex, i, "bas")
            generateResultsDirection(resultArray, board, result, ballPos, ballPosIndex, coupPos, coupIndex, i, "droite")
            generateResultsDirection(resultArray, board, result, ballPos, ballPosIndex, coupPos, coupIndex, i, "gauche")
    return resultArray
    

def algo(board, result, ballPos, ballPosIndex, coupPos, coupIndex):
    if isWin(ballPos, ballPosIndex):
        return True, result
    else:
        for r, ballPosIndexNew, coupPosNew, coupIndexNew in generateResultsFromResult(board, result, ballPos, ballPosIndex, coupPos, coupIndex):
            isWinBool, resultNew = algo(board, r, ballPos, ballPosIndexNew, coupPosNew, coupIndexNew)
            if isWinBool:
                return isWinBool, resultNew
        return False, [[]]

def find_all_balls(texte):
    return [match.start() for match in BALL_PATTERN.finditer(texte)]


if __name__ == "__main__":
    board = []
    ballPos = []
    width, height = [int(i) for i in input().split()]
    for x in range(height):
        row = input()
        board.append(list(row))
        positions = find_all_balls(row)
        for y in positions:
            ballPos.append((x, y))    

    result = [['.' for _ in range(width)] for _ in range(height)]

    _, resultOut = algo(board, result, ballPos, 0, ballPos[0], 0)

    for r in resultOut:
        print("".join(r))