import chess
import datetime

board = chess.Board()

log = open("leafish.log", "w")

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
  5, 10, 10, 10, 10, 10, 10,  5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
  0,  0,  0,  5,  5,  0,  0,  0
]

queentable = [
-20,-10,-10, -5, -5,-10,-10,-20,
-10,  0,  0,  0,  0,  0,  0,-10,
-10,  0,  5,  5,  5,  5,  0,-10,
 -5,  0,  5,  5,  5,  5,  0, -5,
  0,  0,  5,  5,  5,  5,  0, -5,
-10,  5,  5,  5,  5,  5,  0,-10,
-10,  0,  5,  0,  0,  0,  0,-10,
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

def wrapinput():
    global log
    r = input()
    log.write("[in] " + r + "\n")
    return r

def wrapprint(str):
    global log
    log.write("[ou] " + str + "\n")
    print(str)

def evaluate(b):
    pieces = b.piece_map().values()
    score = 0
    piececount = 0
    for piece in pieces:
        side = 1 if piece.color else -1
        score += side * piecevaltable[piece.piece_type]
        if piece.piece_type == chess.QUEEN:
            piececount += 2
        if piece.piece_type != chess.PAWN:
            piececount += 1
    endgame = 1 if piececount < 11 else 0
    for square in chess.SQUARES:
        piece = b.piece_at(square)
        if piece == None:
            continue
        side = 1 if piece.color else -1
        if piece.piece_type == chess.KING:
            score += side * piecepositiontable[chess.KING][endgame][square]
        else:
            score += side * piecepositiontable[piece.piece_type][square]

    return score

def bad3plysearch(b):
    return minimax(b, 4, 1 if b.turn else -1, -20000, 20000)[1]

def minimax(board, depth, side, alpha, beta):
    if board.is_checkmate():
        return (side *  20000, 0)
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

def handle(read):
    global board
    if "ucinewgame" in read:
        board = chess.Board()
    if "go" in read:
        move = bad3plysearch(board)
        wrapprint("bestmove " + str(move))
    if "position" in read:
        if "moves" not in read:
            return
        if "startpos" in read:
            board = chess.Board()
        s1 = read.split(" ")
        s = s1[s1.index("moves") + 1:]

        for move in s:
            if chess.Move.from_uci(move) in board.legal_moves:
                board.push_uci(move)

def main():
    read = wrapinput()

    if "uci" not in read:
        wrapprint("expected uci command!")
        log.close()
        quit()
    wrapprint("uciok")
    wrapprint("id name leafish")
    wrapprint("id author boblovespi")
    # wrapprint("option name MoveOverhead")
    while "isready" not in read:
        read = wrapinput()
        log.write("[in] " + read + "\n")
        if "quit" in read:
            log.close()
            quit()
    wrapprint("readyok")

    while "quit" not in read:
        read = wrapinput()
        handle(read)

    log.close()

if __name__ == "__main__":
    main()