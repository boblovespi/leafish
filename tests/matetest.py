import chess
import searchers
import evaluators
b = chess.Board(fen = "r6k/p1p3pp/8/1p1p1BK1/7r/5P1P/PPQ3P1/4q3 b - - 4 29")
m = searchers.bad3plysearch(b)
print(m)
print(evaluators.simple(b))