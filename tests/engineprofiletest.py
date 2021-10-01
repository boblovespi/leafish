import chess
import searchers
import evaluators
import datetime
import cProfile
import pstats
from pstats import SortKey
import io

board = chess.Board()
board.push_san("Nf3")
board.push_san("d5")
board.push_san("Nc3")
board.push_san("Nf6")

pr = cProfile.Profile()
pr.enable()

for i in range(1, 20):
    time = datetime.datetime.now()
    result = searchers.minimaxquie(evaluators.simple, board, 4, 1 if board.turn else -1, -30000, 30000, quiedepth=4)
    print("move: " + str(result[1]) + " | nodes: " + str(result[2]) + " | eval: " + str(result[0]) + " | time: " + str(datetime.datetime.now() - time))
    board.push(result[1])

pr.disable()
s = io.StringIO()
sortby = SortKey.CUMULATIVE
ps = pstats.Stats(pr, straem = s).sort_stats(sortby)
ps.print_stats()
print("\n\n\n\n")
print(s.getvalue())