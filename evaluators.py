import chess

piecevaltable = {
    chess.PAWN : 100,
    chess.KNIGHT : 320,
    chess.BISHOP : 330,
    chess.ROOK : 500,
    chess.QUEEN : 900,
    chess.KING : 20000
}

pawntable = [
0,  0,  0,  0,  0,  0,  0,  0,
50, 50, 50, 50, 50, 50, 50, 50,
10, 10, 20, 30, 30, 20, 10, 10,
 5,  5, 10, 25, 25, 10,  5,  5,
 0,  0,  0, 20, 20,  0,  0,  0,
 5, -5,-10,  0,  0,-10, -5,  5,
 5, 10, 10,-20,-20, 10, 10,  5,
 0,  0,  0,  0,  0,  0,  0,  0]

knighttable = [
-50,-40,-30,-30,-30,-30,-40,-50,
-40,-20,  0,  0,  0,  0,-20,-40,
-30,  0, 10, 15, 15, 10,  0,-30,
-30,  5, 15, 20, 20, 15,  5,-30,
-30,  0, 15, 20, 20, 15,  0,-30,
-30,  5, 10, 15, 15, 10,  5,-30,
-40,-20,  0,  5,  5,  0,-20,-40,
-50,-40,-30,-30,-30,-30,-40,-50,]

bishoptable = [
-20,-10,-10,-10,-10,-10,-10,-20,
-10,  0,  0,  0,  0,  0,  0,-10,
-10,  0,  5, 10, 10,  5,  0,-10,
-10,  5,  5, 10, 10,  5,  5,-10,
-10,  0, 10, 10, 10, 10,  0,-10,
-10, 10, 10, 10, 10, 10, 10,-10,
-10,  5,  0,  0,  0,  0,  5,-10,
-20,-10,-10,-10,-10,-10,-10,-20,]

rooktable = [
  0,  0,  0,  0,  0,  0,  0,  0,
  5, 20, 20, 20, 20, 20, 20,  5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
  0,  0,  0, 10, 10,  0,  0,  0
]

queentable = [
-20,-10,-10, -5, -5,-10,-10,-20,
-10,  0,  0,  0,  0,  0,  0,-10,
-10,  0,  5,  5,  5,  5,  0,-10,
 -5,  0,  5,  5,  5,  5,  0, -5,
 -5,  0,  5,  5,  5,  5,  0, -5,
-10,  0,  5,  5,  5,  5,  0,-10,
-10,  0,  0,  0,  0,  0,  0,-10,
-20,-10,-10, -5, -5,-10,-10,-20
]

midkingtable = [
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30,
-20,-30,-30,-40,-40,-30,-30,-20,
-10,-20,-20,-20,-20,-20,-20,-10,
 20, 20,  0,  0,  0,  0, 20, 20,
 20, 30, 10,  0,  0, 10, 30, 20
]

endkingtable = [
-50,-40,-30,-20,-20,-30,-40,-50,
-30,-20,-10,  0,  0,-10,-20,-30,
-30,-10, 20, 30, 30, 20,-10,-30,
-30,-10, 30, 40, 40, 30,-10,-30,
-30,-10, 30, 40, 40, 30,-10,-30,
-30,-10, 20, 30, 30, 20,-10,-30,
-30,-30,  0,  0,  0,  0,-30,-30,
-50,-30,-30,-30,-30,-30,-30,-50
]

piecepositiontable = {
    chess.PAWN: pawntable,
    chess.KNIGHT: knighttable,
    chess.BISHOP: bishoptable,
    chess.ROOK: rooktable,
    chess.QUEEN: queentable,
    chess.KING: (midkingtable, endkingtable)
}

def simple(b: chess.Board) -> int:
    score, kingmid, kingend, piececount = 0, 0, 0, 0
    for square, piece in b.piece_map().items():
        side = 1 if piece.color else -1
        score += side * piecevaltable[piece.piece_type]
        if piece.piece_type == chess.QUEEN:
            piececount += 2
        if piece.piece_type != chess.PAWN:
            piececount += 1
        if piece.piece_type == chess.KING:
            kingmid += side * piecepositiontable[chess.KING][0][-side * square]
            kingend += side * piecepositiontable[chess.KING][1][-side * square]
        else:
            score += side * piecepositiontable[piece.piece_type][-side * square]
    return score + (kingend if piececount < 11 else kingmid)

def simplemidend(b: chess.Board, ismid: int) -> int:
    score = 0
    for square, piece in b.piece_map().items():
        side = 1 if piece.color else -1
        score += side * piecevaltable[piece.piece_type]
        if piece.piece_type == chess.KING:
            score += side * piecepositiontable[chess.KING][ismid][-side * square]
        else:
            score += side * piecepositiontable[piece.piece_type][-side * square]
    return score

def incsimple(b: chess.Board, scorein: int, move: chess.Move, ismid: int) -> int:
    piece = b.piece_type_at(move.from_square)
    side = 1 if b.turn else -1
    score = scorein
    if piece == chess.KING:
        score = score - side * piecepositiontable[chess.KING][ismid][-side * move.from_square] + side * piecepositiontable[chess.KING][ismid][-side * move.to_square]
        if move.from_square == chess.E8 and move.to_square == chess.G8:
            score = score - side * piecepositiontable[chess.ROOK][-side * chess.H8] + side * piecepositiontable[chess.ROOK][-side * chess.F8]
        elif move.from_square == chess.E1 and move.to_square == chess.G1:
            score = score - side * piecepositiontable[chess.ROOK][-side * chess.H1] + side * piecepositiontable[chess.ROOK][-side * chess.F1]
        elif move.from_square == chess.E8 and move.to_square == chess.C8:
            score = score - side * piecepositiontable[chess.ROOK][-side * chess.A8] + side * piecepositiontable[chess.ROOK][-side * chess.D8]
        elif move.from_square == chess.E1 and move.to_square == chess.C1:
            score = score - side * piecepositiontable[chess.ROOK][-side * chess.A1] + side * piecepositiontable[chess.ROOK][-side * chess.D1]
    elif move.promotion == None:
        score = score - side * piecepositiontable[piece][-side * move.from_square] + side * piecepositiontable[piece][-side * move.to_square]
    else:
        score = score - side * piecepositiontable[chess.PAWN][-side * move.from_square] - side * piecevaltable[chess.PAWN]
        score = score + side * piecepositiontable[move.promotion][-side * move.to_square] + side * piecevaltable[move.promotion]

    if b.is_capture(move):
        if b.is_en_passant(move):
            score = score + side * piecevaltable[chess.PAWN] + side * piecepositiontable[chess.PAWN][side * (b.ep_square - 8 * side)]
        else:
            score = score + side * piecevaltable[b.piece_type_at(move.to_square)] + side * piecepositiontable[b.piece_type_at(move.to_square)][side * move.to_square]
    return score

def goodcapture(board: chess.Board, move: chess.Move) -> bool:
    if not board.is_capture(move):
        return False
    if board.is_en_passant(move):
        return True
    return (piecevaltable[board.piece_type_at(move.to_square)] - piecevaltable[board.piece_type_at(move.from_square)]) > -300

def ismid(board: chess.Board) -> int:
    piececount = 0
    pieces = board.piece_map().values()
    for piece in pieces:
        if piece.piece_type == chess.QUEEN:
            piececount += 2
        if piece.piece_type != chess.PAWN:
            piececount += 1
    return piececount