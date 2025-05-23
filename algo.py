from main import *


board = [["1", "H"]]
result = [[".", "."]]
holePos = [(0, 0)]
isWinBool, resultOut = algo(board, result, holePos, 0, holePos[0], 0)
