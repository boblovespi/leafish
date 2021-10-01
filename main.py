import chess
import datetime
from searchers import bad3plysearch, bad4plyquiescence

board = chess.Board()

log = open("leafish.log", "w")

def wrapinput():
    global log
    r = input()
    log.write("[in] " + r + "\n")
    log.flush()
    return r

def wrapprint(str):
    global log
    log.write("[ou] " + str + "\n")
    log.flush()
    print(str)

def wraptime(start):
    global log
    log.write("[tm] " + str(datetime.datetime.now() - start) + "\n")
    log.flush()

def handle(read):
    global board
    if "ucinewgame" in read:
        board = chess.Board()
    if "go" in read:
        start = datetime.datetime.now()
        move = bad4plyquiescence(board)
        wrapprint("bestmove " + str(move))
        wraptime(start)
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