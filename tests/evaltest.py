import chess
import searchers
import evaluators
import datetime

b = chess.Board()

t2 = datetime.datetime.now()
for i in range(1, 10000):
	evaluators.simple(b)
print(datetime.datetime.now() - t2)