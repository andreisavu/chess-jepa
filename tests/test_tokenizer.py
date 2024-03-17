from chess_jepa.tokenizer import encode, decode, default_vocabulary


def test_vocabulary():
    assert len(default_vocabulary) == 98


def test_tokenize_only_fen():
    input_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -"
    encoded_fen = encode(input_fen)

    expected = input_fen.replace("8", "." * 8).replace(" ", "")
    assert decode(encoded_fen) == expected


def test_tokenize_masked_uci():
    input_uci = "e2e4 e7e5 ? b8c6 ? d7d6"
    encoded_uci = encode(input_uci)

    expected = input_uci.replace(" ", "")
    assert decode(encoded_uci) == expected


def test_typical_training_example():
    past_uci = "_ _ <s> e2e4 e7e5 ? b8c6 f1c4 d7d6"
    input_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -"
    future_uci = "e1g1 e8g8 <1-0> _ _"

    expected = (
        past_uci.replace(" ", "")
        + input_fen.replace("8", "." * 8).replace(" ", "")
        + future_uci.replace(" ", "")
    ).replace("_", "")

    encoded = encode(past_uci + " " + input_fen + " " + future_uci)
    assert decode(encoded).replace("_", "") == expected
