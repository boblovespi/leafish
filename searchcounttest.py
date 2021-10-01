import chess
import searchers
import evaluators
import datetime
import cProfile
import io
import pstats
from pstats import SortKey

t1 = datetime.datetime.now()
b = chess.Board()
b.push_san("Nf3")
b.push_san("d5")
# pr = cProfile.Profile()
# pr.enable()
print(searchers.minimaxquie(evaluators.simple, b, 4, 1 if b.turn else -1, -30000, 30000, quiedepth=2))
print (datetime.datetime.now() - t1)
# pr.disable()
# s = io.StringIO()
# sortby = SortKey.CUMULATIVE
# ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
# ps.print_stats()
# print(s.getvalue())
t2 = datetime.datetime.now()
# print(searchers.minimaxquie(evaluators.simple, b, 5, b.turn, -30000, 30000, False, quiedepth=1))
# print (datetime.datetime.now() - t2)
# t2 = datetime.datetime.now()
print(searchers.minimaxquie(evaluators.simple, b, 3, b.turn, -30000, 30000, False, quiedepth=3))
print(datetime.datetime.now() - t2)

t2 = datetime.datetime.now()
# for i in range(1, 500000):
# 	evaluators.simple(b)
print(datetime.datetime.now() - t2)