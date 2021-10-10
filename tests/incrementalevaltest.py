import chess
import evaluators
import searchers
import datetime

board = chess.Board()

score = evaluators.simple(board)

for i in range(1, 50):
    time = datetime.datetime.now()
    result = searchers.minimaxquie(evaluators.simple, board, 4, 1 if board.turn else -1, -30000, 30000, quiedepth=0)
    s1 = evaluators.incsimple(board, score, result[1], 0)
    board.push(result[1])
    print("move: " + str(result[1]) + " | nodes: " + str(result[2]) + " | eval: " + str(result[0]) + " | time: " + str(datetime.datetime.now() - time) + " | inc eval: " + str(s1) + " | reg eval: " + str(evaluators.simplemidend(board, 0)))
    score = s1