"""
Handcrafted tokenizer. This is as minimal as it can be for the game of chess.
"""


class Vocabulary:
    def __init__(self, padding_token):
        self.token_to_index = {}
        self.index_to_token = {}
        self.add_token(padding_token)

    def add_token(self, token: str):
        if token not in self.token_to_index:
            index = len(self.token_to_index)
            self.token_to_index[token] = index
            self.index_to_token[index] = token

    def get_index(self, token: str) -> int:
        return self.token_to_index[token]

    def get_token(self, index: int) -> str:
        return self.index_to_token[index]

    def __contains__(self, token: str) -> bool:
        return token in self.token_to_index

    def __len__(self):
        return len(self.token_to_index)


_castling_rights = [
    "-",  # No castling rights
    "K",  # White can castle kingside
    "Q",  # White can castle queenside
    "KQ",  # White can castle both kingside and queenside
    "k",  # Black can castle kingside
    "Kk",  # White can castle kingside, Black can castle kingside
    "Qk",  # White can castle queenside, Black can castle kingside
    "KQk",  # White can castle both kingside and queenside, Black can castle kingside
    "q",  # Black can castle queenside
    "Kq",  # White can castle kingside, Black can castle queenside
    "Qq",  # White can castle queenside, Black can castle queenside
    "KQq",  # White can castle both kingside and queenside, Black can castle queenside
    "kq",  # Black can castle both kingside and queenside
    "Kkq",  # White can castle kingside, Black can castle both kingside and queenside
    "Qkq",  # White can castle queenside, Black can castle both kingside and queenside
    "KQkq",  # Both sides can castle both kingside and queenside
]


def _initialize_default_vocabulary() -> Vocabulary:
    """
    Initializes the vocabulary with the default tokens.
    """
    vocab = Vocabulary(padding_token="<_>")

    vocab.add_token("<start>")  # Start of the game
    vocab.add_token("<1-0>")  # White wins
    vocab.add_token("<0-1>")  # Black wins
    vocab.add_token("<1/2-1/2>")  # Draw
    vocab.add_token("<*>")  # Unknown result (abandoned game, etc.)

    # All chess pieces in the standard FEN notation
    for piece in "rnbqkpRNBQKP":
        vocab.add_token(piece)

    vocab.add_token(".")  # Empty squares
    vocab.add_token("/")  # Separator between ranks

    vocab.add_token("w")  # White to move
    vocab.add_token("b")  # Black to move

    # No en passant square or no castling rights
    vocab.add_token("-")

    # Castling rights in the standard FEN notation (KQkq)
    for rights in _castling_rights:
        vocab.add_token(rights)

    # All the squares in the standard UCI notation
    for file in "abcdefgh":
        for rank in "12345678":
            vocab.add_token(file + rank)

    # All the possible moves in the standard UCI notation
    for file1 in "abcdefgh":
        for rank1 in "12345678":
            for file2 in "abcdefgh":
                for rank2 in "12345678":
                    vocab.add_token(file1 + rank1 + file2 + rank2)

    # Masked move (used during training to mask the target move in the input sequence)
    vocab.add_token("?")

    return vocab


default_vocabulary = _initialize_default_vocabulary()


def encode(input: str) -> list[int]:
    """
    Encodes the input string into a list of tokens. Warning: Not symmetric with decode.
    """
    result = []
    for word in input.split(" "):
        if word in default_vocabulary:
            result.append(default_vocabulary.get_index(word))
        else:
            assert "/" in word, f"Unknown token: {word}"
            # If the word is not in the vocabulary, encode it character by character
            for char in word:
                if char.isdigit():
                    # Handle normal FEN notation (digits represent empty squares)
                    # Expand into the corresponding number of empty squares
                    for _ in range(int(char)):
                        result.append(default_vocabulary.get_index("."))
                else:
                    result.append(default_vocabulary.get_index(char))
    return result


def decode(input: list[int]) -> str:
    """
    Decodes the list of tokens into a string. Warning: Not symmetric with encode.
    """
    return "".join(default_vocabulary.get_token(index) for index in input)
