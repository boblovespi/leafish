import chess
import evaluators

def bad3plysearch(board: chess.Board, evaluator = evaluators.simple) -> chess.Move:
    return minimax(evaluator, board, 4, 1 if board.turn else -1, -20000, 20000)[1]

def minimax(f, board, depth, side, alpha, beta):
    if board.is_checkmate():
        return (side *  (-20000 - depth), 0)
    if board.is_stalemate():
        return (0, 0)
    if depth == 0:
        return (side * f(board), 0)
    val = -20000
    m1 = next(iter(board.generate_legal_moves()))
    for m in board.generate_legal_moves():
        b1 = board.copy(stack = False)
        b1.push(m)
        val1 = -minimax(f, b1, depth - 1, -side, -beta, -alpha)[0]
        m1 = m if val1 > val else m1
        val = val1 if val1 > val else val
        alpha = max(alpha, val)
        if alpha >= beta:
            break
    return (val, m1)