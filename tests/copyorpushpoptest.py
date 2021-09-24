import chess
from datetime import datetime

def copysearch(b: chess.Board, d):
    if d == 0:
        return 1
    n = 0
    for m in b.legal_moves:
        b1 = b.copy(stack = False)
        b1.push(m)
        n += copysearch(b1, d - 1)
    return n

def pushpopsearch(b: chess.Board, d):
    if d == 0:
        return 1
    n = 0
    for m in b.legal_moves:
        b.push(m)
        n += copysearch(b, d - 1)
        b.pop()
    return n

def time(b, search, d):
    print(str(search))
    now = datetime.now()
    print(search(b, d))
    print(datetime.now() - now)

board = chess.Board()
time(board, copysearch, 3)
board = chess.Board()
time(board, pushpopsearch, 3)
fen = "6n1/1p3p2/3p1kp1/4p3/3P4/1PK1P3/2P3P1/1N6 w - - 0 1"
board = chess.Board(fen = fen)
time(board, copysearch, 4)
board = chess.Board(fen = fen)
time(board, pushpopsearch, 4)
fen = "3k4/3p4/8/8/8/8/3P4/3K4 w - - 0 1"
board = chess.Board(fen = fen)
time(board, copysearch, 5)
board = chess.Board(fen = fen)
time(board, pushpopsearch, 5)
fen = "8/8/8/1p6/1k6/pP6/P7/K7 w - - 0 1"
board = chess.Board(fen = fen)
time(board, copysearch, 10)
board = chess.Board(fen = fen)
time(board, pushpopsearch, 10)