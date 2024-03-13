import argparse
import logging
import numpy as np
import random
import sys

from chess_jepa.tokenizer import encode
from chess_jepa.pgn import extract_training_samples


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pgn", required=True, help="input file path")
    parser.add_argument("--train", default="train.bin", help="train output file path")
    parser.add_argument("--eval", default="eval.bin", help="eval output file path")
    args = parser.parse_args()

    # Configure logging to stdout
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    # Initialize token counters
    train_tokens = 0
    eval_tokens = 0

    # Read the PGN file and extract the training samples
    with open(args.pgn, "r") as file:
        logging.info(f"Reading PGN file: {args.pgn}")
        # Throw a dice to decide if the sample goes to the training or evaluation set
        use_for_train = random.random() < 0.8
        with open(args.train, "ab") as train_file:
            with open(args.eval, "ab") as eval_file:
                for index, sample in enumerate(extract_training_samples(file, window_size=5)):
                    tokens = np.array(encode(sample))
                    if index == 0:
                        logging.info(f"Sample tokens length: {len(tokens)}")
                    if use_for_train:
                        tokens.tofile(train_file)
                        train_tokens += len(tokens)
                    else:
                        tokens.tofile(eval_file)
                        eval_tokens += len(tokens)

    # Report token statistics
    logging.info(f"Total tokens persisted to train.bin: {train_tokens}")
    logging.info(f"Total tokens persisted to eval.bin: {eval_tokens}")


if __name__ == "__main__":
    main()
