"""
Handcrafted tokenizer. This is as minimal as it can be for the game of chess.
"""

PADDING_TOKEN = "_"
START_TOKEN = "<s>"


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
    vocab = Vocabulary(padding_token=PADDING_TOKEN)

    vocab.add_token(START_TOKEN)  # Start of the game
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

    # For all ranks, when on the first (1) or last (8) file, encode the promotion moves
    for file in "abcdefgh":
        for piece in "qrbn":
            # Black pieces in lowercase
            vocab.add_token(file + "1" + piece)
            vocab.add_token(file + "8" + piece)
            # And uppercase for the white pieces
            vocab.add_token(file + "1" + piece.upper())
            vocab.add_token(file + "8" + piece.upper())

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
            # In order to make the context window size fixed, we add the padding token
            # before the start token and after the end game tokens. This way, all the
            # tokens outside outside of FEN and UCI moves will use two tokens. Yeah, this
            # is a bit of a hack, but it works.
            if word == PADDING_TOKEN:
                result.append(default_vocabulary.get_index(word))
            if word == START_TOKEN:
                result.append(default_vocabulary.get_index(PADDING_TOKEN))
            result.append(default_vocabulary.get_index(word))
            if word != START_TOKEN and word.startswith("<") and word.endswith(">"):
                result.append(default_vocabulary.get_index(PADDING_TOKEN))
        elif len(word) == 4 or len(word) == 5 and word[4] in "qrbn":
            # this is an UCI formatted move - generate two tokens
            result.append(default_vocabulary.get_index(word[:2]))
            result.append(default_vocabulary.get_index(word[2:]))
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
