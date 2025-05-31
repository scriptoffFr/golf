import sys
import math
import re
from copy import deepcopy

DIRECTIONS = {
    "haut":    {"dx": -1, "dy":  0, "char": "^", "invChar": "v", "inverseDirection": "bas"},
    "bas":     {"dx":  1, "dy":  0, "char": "v", "invChar": "^", "inverseDirection": "haut"},
    "gauche":  {"dx":  0, "dy": -1, "char": "<", "invChar": ">", "inverseDirection": "droite"},
    "droite":  {"dx":  0, "dy":  1, "char": ">", "invChar": "<", "inverseDirection": "gauche"},
}

BALL_PATTERN = re.compile(r"[1-9]")

def isWin(ballPos, ballPosIndex):
    return ballPosIndex == len(ballPos) 

def generateResultsDirection(resultArray, board, result, ballPos, ballPosIndex, coupPos, coupIndex, nbCases, direction, oldDirection):
    dx = DIRECTIONS[direction]["dx"]
    dy = DIRECTIONS[direction]["dy"]
    char = DIRECTIONS[direction]["char"]
    inverseDirection = DIRECTIONS[direction]["inverseDirection"]

    valide = True
    resultNew = deepcopy(result)
    ballPosIndexNew = ballPosIndex
    coupIndexNew = coupIndex + 1
    x, y = coupPos
    coupPos_x, couPos_y = coupPos
    ballPos_x, ballPos_y = ballPos[ballPosIndex]
    rows, cols = len(board), len(board[0])
    nbCasesNew = nbCases
    oldDirectionNew = direction

    if (direction == "haut" and x == 0) or \
        (direction == "bas" and x == rows - 1) or \
        (direction == "gauche" and y == 0) or \
        (direction == "droite" and y == cols - 1) or \
        (direction == oldDirection) or \
        (inverseDirection == oldDirection):
            return

    while nbCasesNew > 0 and 0 <= x < rows and 0 <= y < cols:
        cell_result = result[x][y]
        cell_board = board[x][y]
        next_x, next_y = x + dx, y + dy
        resultNew[x][y] = char
        coupPosNew = (next_x,next_y) if 0 <= next_x < rows and 0 <= next_y < cols else (x,y)
        
        if nbCases == 1 and cell_board == "X":
            valide = False
            break

        if (x,y) != (ballPos_x, ballPos_y) and '1' <= cell_board <= '9':
            valide = False
            break
        
        if cell_result in {"^", "v", "<", ">"}:
            valide = False
            break

        if 0 <= next_x < rows and 0 <= next_y < cols and board[next_x][next_y] == "H":
            occupe = False
            for d in DIRECTIONS.keys():
                around_x = next_x+DIRECTIONS[d]["dx"]
                around_y = next_y+DIRECTIONS[d]["dy"]
                if 0 <= around_x < rows and 0 <= around_y < cols and \
                result[around_x][around_y] == DIRECTIONS[d]["invChar"]:
                    occupe = True
            if occupe:
                valide = False
                break
            else:    
                ballPosIndexNew = ballPosIndex + 1
                coupIndexNew  = 0
                oldDirectionNew = None
                coupPosNew = ballPos[ballPosIndexNew] if ballPosIndexNew < len(ballPos) else None
                break

        x += dx
        y += dy
        nbCasesNew -= 1
    if valide:
        resultArray.append((resultNew, ballPosIndexNew, coupPosNew, coupIndexNew, oldDirectionNew))


def generateResultsFromResult(board, result, ballPos, ballPosIndex, coupPos, coupIndex, oldDirection):
    resultArray = []
    ballPos_x, ballPos_y = ballPos[ballPosIndex]
    nbMaxCoup = int(board[ballPos_x][ballPos_y])
    if coupIndex < nbMaxCoup:
        nbCases = nbMaxCoup - coupIndex
        generateResultsDirection(resultArray, board, result, ballPos, ballPosIndex, coupPos, coupIndex, nbCases, "haut", oldDirection)
        generateResultsDirection(resultArray, board, result, ballPos, ballPosIndex, coupPos, coupIndex, nbCases, "bas", oldDirection)
        generateResultsDirection(resultArray, board, result, ballPos, ballPosIndex, coupPos, coupIndex, nbCases, "droite", oldDirection)
        generateResultsDirection(resultArray, board, result, ballPos, ballPosIndex, coupPos, coupIndex, nbCases, "gauche", oldDirection)
    return resultArray
    

def algo(board, result, ballPos, ballPosIndex, coupPos, coupIndex, oldDirection):
    if isWin(ballPos, ballPosIndex):
        return True, result
    else:
        for r, ballPosIndexNew, coupPosNew, coupIndexNew, oldDirectionNew in generateResultsFromResult(board, result, ballPos, ballPosIndex, coupPos, coupIndex, oldDirection):
            isWinBool, resultNew = algo(board, r, ballPos, ballPosIndexNew, coupPosNew, coupIndexNew, oldDirectionNew)
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

    _, resultOut = algo(board, result, ballPos, 0, ballPos[0], 0, None)

    for r in resultOut:
        print("".join(r))