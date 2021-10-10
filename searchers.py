import chess
import evaluators

class Searcher:
    def __init__(self, board: chess.Board, callback, stopcheck = lambda : False, evaluator = evaluators.incsimple, depth: int = 4, usequiescence: bool = True, quiescencedepth: int = 4):
        self.board = board
        self.bestmove = chess.Move.null()
        self._stopcheck = stopcheck
        self._f = evaluator
        self._d = depth
        self._useq = usequiescence
        self._qd = quiescencedepth
        self._callback = callback
        self._sm = evaluators.simplemidend(board, 0)
        self._se = evaluators.simplemidend(board, 1)
        self._pc = evaluators.ismid(board)

    def start(self):
        move = self.minimaxquieinc(self._f, self.board, self._d, 1 if self.board.turn else -1, -30000, 30000, quiedepth=self._qd, piececount=self._pc, sm=self._sm, se=self._se)
        self.bestmove = move[1]
        self._callback(move[1])

    def minimaxquieinc(self, f, board, depth, side, alpha, beta, isquie = False, quiedepth = 4, piececount = 0, sm = 0, se = 0, root = True):
        if depth == 0:
            if isquie:
                return (side * (se if piececount < 11 else sm) , 0, 1, False)
            else:
                return self.minimaxquieinc(f, board, quiedepth, side, alpha, beta, True, 0, piececount, sm, se, False)
        moves = board.legal_moves
        if not any(moves):
            if board.is_check(): # checkmate
                return ((-20000 - depth - quiedepth), 0, 1, False)
            else: # stalemate
                return (0, 0, 1, False)
        val = -30000 if not isquie else side * (se if piececount < 11 else sm)
        c = 0
        m1 = 0
        earlybreak = False
        for m in moves:
            if self._stopcheck():
                return (val, m1, c, True)
            shouldcheck = not isquie or m.promotion == chess.QUEEN or evaluators.goodcapture(board, m)
            sm1 = f(board, sm, m, 0)
            se1 = f(board, se, m, 1)
            pc1 = piececount
            if board.is_capture(m) and not board.is_en_passant(m):
                pt = board.piece_type_at(m.to_square)
                if pt == chess.QUEEN:
                    pc1 -= 2
                if pt != chess.PAWN:
                    pc1 -= 1
            board.push(m)
            if not shouldcheck and not board.is_check():
                board.pop()
                continue
            c += 1
            ret = self.minimaxquieinc(f, board, depth - 1, -side, -beta, -alpha, isquie, quiedepth, pc1, sm1, se1, False)
            board.pop()
            earlybreak = ret[3]
            val1 = -ret[0]
            c += ret[2]
            m1 = m if val1 > val else m1
            val = val1 if val1 > val else val
            if root:
                self.bestmove = m1
            alpha = max(alpha, val)
            if alpha >= beta:
                break
            if earlybreak:
                break
        return (val, m1, c, earlybreak)

    


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
    if depth == 0:
        if isquie:
            return (side * f(board), 0, 1)
        else:
            return minimaxquie(f, board, quiedepth, side, alpha, beta, True, 0)
    moves = board.legal_moves
    if not any(moves):
        if board.is_check(): # checkmate
            return ((-20000 - depth - quiedepth), 0, 1)
        else: # stalemate
            return (0, 0, 1)
    val = -30000 if not isquie else side * f(board)
    c = 0
    m1 = 0
    for m in moves:
        shouldcheck = not isquie or m.promotion == chess.QUEEN or evaluators.goodcapture(board, m)
        board.push(m)
        if not shouldcheck and not board.is_check():
            board.pop()
            continue
        c += 1
        ret = minimaxquie(f, board, depth - 1, -side, -beta, -alpha, isquie, quiedepth)
        board.pop()
        val1 = -ret[0]
        c += ret[2]
        m1 = m if val1 > val else m1
        val = val1 if val1 > val else val
        alpha = max(alpha, val)
        if alpha >= beta:
            break
    return (val, m1, c)

def minimaxquieinc(f, board, depth, side, alpha, beta, isquie = False, quiedepth = 4, piececount = 0, sm = 0, se = 0):
    moves = board.legal_moves
    if not any(moves):
        if board.is_check(): # checkmate
            return ((-20000 - depth - quiedepth), 0, 1)
        else: # stalemate
            return (0, 0, 1)
    if depth == 0:
        if isquie:
            return (side * (se if piececount < 11 else sm) , 0, 1)
        else:
            return minimaxquieinc(f, board, quiedepth, side, alpha, beta, True, 0, piececount, sm, se)
    val = -30000 if not isquie else side * (se if piececount < 11 else sm)
    c = 0
    m1 = 0
    for m in moves:
        shouldcheck = not isquie or m.promotion == chess.QUEEN or evaluators.goodcapture(board, m)
        sm1 = f(board, sm, m, 0)
        se1 = f(board, se, m, 1)
        pc1 = piececount
        if board.is_capture(m) and not board.is_en_passant(m):
            pt = board.piece_type_at(m.to_square)
            if pt == chess.QUEEN:
                pc1 -= 2
            if pt != chess.PAWN:
                pc1 -= 1
        board.push(m)
        if not shouldcheck and not board.is_check():
            board.pop()
            continue
        c += 1
        ret = minimaxquieinc(f, board, depth - 1, -side, -beta, -alpha, isquie, quiedepth, pc1, sm1, se1)
        board.pop()
        val1 = -ret[0]
        c += ret[2]
        m1 = m if val1 > val else m1
        val = val1 if val1 > val else val
        alpha = max(alpha, val)
        if alpha >= beta:
            break
    return (val, m1, c)