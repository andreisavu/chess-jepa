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

    # Window size for the training samples
    default_window_size = 7

    # Read the PGN file and extract the training samples
    with open(args.pgn, "r") as file:
        logging.info(f"Reading PGN file: {args.pgn}")

        with open(args.train, "ab") as train_file:
            with open(args.eval, "ab") as eval_file:
                for index, sample in enumerate(extract_training_samples(file, default_window_size)):
                    # Throw a dice to decide if the sample goes to the training or evaluation set
                    use_for_train = random.random() < 0.9

                    tokens = np.array(encode(sample), dtype=np.int32)
                    header = np.array([len(tokens), default_window_size], dtype=np.int32)
                    
                    if index == 0:
                        logging.info(f"Sample header: {header}")
                    
                    if use_for_train:
                        header.tofile(train_file)
                        tokens.tofile(train_file)
                        train_tokens += len(tokens)
                    else:
                        header.tofile(eval_file)
                        tokens.tofile(eval_file)
                        eval_tokens += len(tokens)

                    if index % 10_000 == 0:
                        logging.info(f"Processed {index} samples. Train tokens: {train_tokens}, Eval tokens: {eval_tokens}")

                    if index > 1000_000:
                        break # Limit the number of samples to process to 1M

    # Report token statistics
    logging.info(f"Total tokens persisted to train.bin: {train_tokens}")
    logging.info(f"Total tokens persisted to eval.bin: {eval_tokens}")


if __name__ == "__main__":
    main()
