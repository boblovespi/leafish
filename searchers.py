import chess
import evaluators

def bad3plysearch(board: chess.Board, evaluator = evaluators.simple) -> chess.Move:
    return minimax(evaluator, board, 4, 1 if board.turn else -1, -30000, 30000)[1]

def bad4plyquiescence(board: chess.Board, evaluator = evaluators.simple) -> chess.Move:
    return minimaxquie(evaluator, board, 4, 1 if board.turn else -1, -30000, 30000, False, 2)[1]

def minimax(f, board, depth, side, alpha, beta):
    if board.is_checkmate():
        return ((-20000 - depth), 0, 1)
    if board.is_stalemate():
        return (0, 0, 1)
    if depth == 0:
        return (side * f(board), 0, 1)
    val = -30000
    c = 0
    m1 = next(iter(board.generate_legal_moves()))
    for m in board.generate_legal_moves():
        b1 = board.copy(stack = False)
        b1.push(m)
        ret = minimax(f, b1, depth - 1, -side, -beta, -alpha)
        val1 = -ret[0]
        c += ret[2]
        m1 = m if val1 > val else m1
        val = val1 if val1 > val else val
        alpha = max(alpha, val)
        if alpha >= beta:
            break
    return (val, m1, c)

def minimaxquie(f, board, depth, side, alpha, beta, isquie = False, quiedepth = 4):
    if board.is_checkmate():
        return ((-20000 - depth - quiedepth), 0, 1)
    if board.is_stalemate():
        return (0, 0, 1)
    if depth == 0:
        if isquie:
            return (side * f(board), 0, 1)
        else:
            return minimaxquie(f, board, quiedepth, side, alpha, beta, True, 0)
    val = -30000 if not isquie else side * f(board)
    c = 0
    m1 = 0
    for m in board.legal_moves:
        if not isquie or m.promotion == chess.QUEEN or board.gives_check(m) or evaluators.goodcapture(board, m):
            c += 1
            b1 = board.copy(stack = False)
            b1.push(m)
            ret = minimaxquie(f, b1, depth - 1, -side, -beta, -alpha, isquie, quiedepth)
            val1 = -ret[0]
            c += ret[2]
            m1 = m if val1 > val else m1
            val = val1 if val1 > val else val
            alpha = max(alpha, val)
            if alpha >= beta:
                break
    return (val, m1, c)