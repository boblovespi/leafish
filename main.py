import chess
import datetime
from searchers import bad3plysearch, bad4plyquiescence, Searcher
import threading

board = chess.Board()
alertstop = False

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

def handlemove(move, start):
    global alertstop
    wrapprint("bestmove " + str(move))
    wraptime(start)
    alertstop = False

def handle(read):
    global board, alertstop
    if "ucinewgame" in read:
        board = chess.Board()
    if "go" in read:
        start = datetime.datetime.now()
        searcher = Searcher(board.copy(stack=False), lambda m : handlemove(m, start), lambda : alertstop)
        searchthread = threading.Thread(target = searcher.start)
        searchthread.start()
        
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
    if "stop" in read:
        alertstop = True

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