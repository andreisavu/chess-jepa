
from chess_jepa.tokenizer import encode, decode

def main():
    # This is a dummy example
    input = "rnbqkbnr/pppppppp/......../......../......../......../PPPPPPPP/RNBQKBNR w KQkq - e2e4 e7e5 ? b8c6 ? d7d6 w/b/d"
    encoded = encode(input)
    print(encoded)
    decoded = decode(encoded)
    print(decoded)

if __name__ == "__main__":
    main()
