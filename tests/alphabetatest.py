import chess
import main
import datetime

piecevaltable = {
    chess.PAWN : 100,
    chess.KNIGHT : 320,
    chess.BISHOP : 330,
    chess.ROOK : 500,
    chess.QUEEN : 900,
    chess.KING : 20000
}

def evaluate(b):
    pieces = b.piece_map().values()
    score = 0
    for piece in pieces:
        side = 1 if piece.color else -1
        score += side * piecevaltable[piece.piece_type]
    return score

def bad3plysearch(b, n):
    return minimaxab(b, n, 1 if b.turn else -1, -20000, 20000)

def minimaxab(board, depth, side, alpha, beta):
    if board.is_checkmate():
        return side * -20000
    if depth == 0:
        return side * evaluate(board)
    val = -20000
    for m in board.generate_legal_moves():
        b1 = board.copy(stack = False)
        b1.push(m)
        val = max(val, -minimaxab(b1, depth - 1, -side, -beta, -alpha))
        alpha = max(alpha, val)
        if alpha >= beta:
            break
    return val

def minimax(board, depth, side, alpha, beta):
    if board.is_checkmate():
        return (side * 20000, 0)
    if depth == 0:
        return (side * evaluate(board), 0)
    val = -20000
    m1 = next(iter(board.generate_legal_moves()))
    for m in board.generate_legal_moves():
        b1 = board.copy(stack = False)
        b1.push(m)
        val1 = -minimax(b1, depth - 1, -side, -beta, -alpha)[0]
        m1 = m if val1 > val else m1
        val = val1 if val1 > val else val
        alpha = max(alpha, val)
        if alpha >= beta:
            break
    return (val, m1)

board = chess.Board(fen = "rnbqkb2/pppppp1p/7p/4P1r1/2BP3N/2N2Q2/PPP2P1P/R3K2R b KQq - 3 9")
print(bad3plysearch(board, 3))

print(evaluate(board))

print(minimax(board, 4, 1 if board.turn else -1, -20000, 20000))