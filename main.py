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

def generateResultsDirection(resultArray, board, result, ballPos, ballPosIndex, coupPos, coupIndex, direction):
    dx = DIRECTIONS[direction]["dx"]
    dy = DIRECTIONS[direction]["dy"]
    char = DIRECTIONS[direction]["char"]

    valide = True
    resultNew = deepcopy(result)
    ballPosIndexNew = ballPosIndex
    coupIndexNew = coupIndex + 1
    x, y = coupPos
    rows, cols = len(board), len(board[0])

    while 0 <= x < rows and 0 <= y < cols:
        cell_result = result[x][y]
        cell_board = board[x][y]
        
        if (dx != 0 and (x == 0 or x == rows - 1)) or \
        (dy != 0 and (y == 0 or y == cols - 1)):
            coupPosNew = (x,y)
            if cell_board == "X":
                valide = False
                break

        if cell_result in {"^", "v", "<", ">"} or ('1' <= cell_board <= '9'):
            valide = False
            break

        if cell_board == "H":
            occupe = False
            for d in DIRECTIONS.keys():
                if d != direction and board[x+DIRECTIONS[d]["dx"]][y+DIRECTIONS[d]["dy"]] == DIRECTIONS[d]["invChar"]:
                    occupe = True
            if occupe:
                valide = False
                break
            else:
                ballPosIndexNew = ballPosIndex + 1
                coupPosNew = ballPos[ballPosIndexNew]
                break

        resultNew[x][y] = char
        x += dx
        y += dy

    if valide:
        resultArray.append(resultNew, ballPosIndexNew, coupPosNew, coupIndexNew)


def generateResultsFromResult(board, result, ballPos, ballPosIndex, coupPos, coupIndex):
    resultArray = []
    ballPos_x, ballPos_y = ballPos[ballPosIndex]
    nbMaxCoup = int(board[ballPos_x][ballPos_y])
    if coupIndex < nbMaxCoup:
        generateResultsDirection(resultArray, board, result, ballPos, ballPosIndex, coupPos, coupIndex, "haut")
        generateResultsDirection(resultArray, board, result, ballPos, ballPosIndex, coupPos, coupIndex, "bas")
        generateResultsDirection(resultArray, board, result, ballPos, ballPosIndex, coupPos, coupIndex, "droite")
        generateResultsDirection(resultArray, board, result, ballPos, ballPosIndex, coupPos, coupIndex, "gauche")
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
    for y in range(height):
        row = input()
        board.append(list(row))
        positions = find_all_balls(row)
        for x in positions:
            ballPos.append((x, y))    

    result = [['.' for _ in range(width)] for _ in range(height)]

    _, resultOut = algo(board, result, ballPos, 0, ballPos[0], 0)

    for r in resultOut:
        print("".join(r))