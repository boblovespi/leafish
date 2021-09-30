import chess
import chess.engine

engine = chess.engine.SimpleEngine.popen_uci("./lichess-bot-master/engines/leafish/main")

board = chess.Board()

while not board.is_game_over():
    result = engine.play(board, chess.engine.Limit(time = 100))
    board.push(result.move)

engine.quit()