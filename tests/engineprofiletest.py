import chess
import searchers
import evaluators
import datetime
import cProfile
import pstats
from pstats import SortKey
import io

board = chess.Board(fen = "r1bqk2r/ppp2ppp/2p5/2b5/2B1P1n1/2NP4/PPP2PPP/R1BQK2R w KQkq - 0 1")

pr = cProfile.Profile()
pr.enable()

for i in range(1, 3):
    time = datetime.datetime.now()
    result = searchers.minimaxquie(evaluators.simple, board, 4, 1 if board.turn else -1, -30000, 30000, quiedepth=2)
    # result = searchers.minimaxquieinc(evaluators.incsimple, board, 4, 1 if board.turn else -1, -30000, 30000, quiedepth=2, piececount=evaluators.ismid(board), sm=evaluators.simplemidend(board, 0), se=evaluators.simplemidend(board, 1))
    print("move: " + str(result[1]) + " | nodes: " + str(result[2]) + " | eval: " + str(result[0]) + " | time: " + str(datetime.datetime.now() - time))
    board.push(result[1])

pr.disable()
s = io.StringIO()
sortby = SortKey.CUMULATIVE
ps = pstats.Stats(pr, stream = s).sort_stats(sortby)
ps.print_stats()
print("\n\n\n\n")
print(s.getvalue())