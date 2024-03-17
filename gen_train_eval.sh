#!/usr/bin/env bash
rm data/*.bin
python pgn_to_bin.py --pgn data/lichess_elite_2024-02.pgn --train data/train.bin --eval data/eval.bin
