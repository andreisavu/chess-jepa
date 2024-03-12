
from chess_jepa.tokenizer import encode, decode

def main():
    # This is a dummy example
    input = "e2e4"
    encoded = encode(input)
    print(encoded)
    decoded = decode(encoded)
    print(decoded)

if __name__ == "__main__":
    main()
