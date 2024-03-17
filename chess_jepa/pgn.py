import io
import chess
import chess.pgn

from .tokenizer import PADDING_TOKEN, START_TOKEN


def extract_training_samples(input, window_size=5):
    if isinstance(input, str):
        input = io.StringIO(input)
    game = chess.pgn.read_game(input)
    moves = list(game.mainline_moves())
    board = game.board()

    before_moves = [
        PADDING_TOKEN,
    ] * (window_size - 1) + [
        START_TOKEN,
    ]
    after_moves = []

    # Play all the moves and fill the after buffer
    for move in moves:
        if len(after_moves) < window_size:
            after_moves.append(move.uci())
        else:
            before_moves.pop(0)

            move_to_play = after_moves.pop(0)
            board.push(chess.Move.from_uci(move_to_play))

            before_moves.append(move_to_play)
            after_moves.append(move.uci())

        trimed_fen = board.fen().split(" ")[:-2]
        yield " ".join(
            before_moves
            + trimed_fen
            + after_moves
            + [PADDING_TOKEN, ] * (window_size - len(after_moves))
        )

    # Play all the moves left in the after buffer
    outcome_token = "<" + game.headers["Result"] + ">"
    for index in range(len(after_moves)):
        before_moves.pop(0)

        move_to_play = after_moves.pop(0)
        board.push(chess.Move.from_uci(move_to_play))

        before_moves.append(move_to_play)
        after_moves.append(outcome_token if index == 0 else PADDING_TOKEN)

        trimed_fen = board.fen().split(" ")[:-2]
        yield " ".join(
            before_moves
            + trimed_fen
            + after_moves
            + [
                PADDING_TOKEN,
            ]
            * (window_size - len(after_moves))
        )
