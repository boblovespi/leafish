import chess
import datetime
from searchers import bad3plysearch, bad4plyquiescence, Searcher
import threading
from time import sleep

board = chess.Board()
alertstop = False

log = open("leafish.log", "w")

def wrapinput():
    global log
    r = input()
    log.write("[in] " + r + "\n")
    log.flush()
    return r

def wrapprint(string):
    global log
    print(string, flush = True)
    log.write("[ou] " + string + "\n")
    log.flush()

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
        s1 = read.split(" ")
        stop = lambda : alertstop
        mtime = -1
        if "movetime" in read:
            mtime = int(s1[s1.index("movetime") + 1]) * 0.001 * 0.95
        if board.turn and "wtime" in read:
            mtime = int(s1[s1.index("wtime") + 1]) * 0.001 * 0.2
        if not board.turn and "btime" in read:
            mtime = int(s1[s1.index("btime") + 1]) * 0.001 * 0.2
        start = datetime.datetime.now()
        searcher = Searcher(board, lambda m : handlemove(m, start), stop, maxtime=mtime)
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