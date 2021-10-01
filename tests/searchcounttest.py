import chess
import searchers
import evaluators
import datetime

t1 = datetime.datetime.now()
b = chess.Board()
b.push_san("Nf3")
b.push_san("d5")
print(searchers.minimaxquie(evaluators.simple, b, 4, 1 if b.turn else -1, -30000, 30000, quiedepth=4))
print(datetime.datetime.now() - t1)
t2 = datetime.datetime.now()
# print(searchers.minimaxquie(evaluators.simple, b, 5, b.turn, -30000, 30000, False, quiedepth=1))
# print (datetime.datetime.now() - t2)
# t2 = datetime.datetime.now()
print(searchers.minimaxquie(evaluators.simple, b, 3, b.turn, -30000, 30000, False, quiedepth=3))
print(datetime.datetime.now() - t2)