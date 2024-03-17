# Chess-JEPA 
Exploring JEPA (Joint-Embedding Predictive Architecture) and related techniques in the world of chess to learn an algorithm that can construct a useful representation for long term planning (e.g. think N moves in advance)

## Training Data

The main data source for this exploration is https://database.lichess.org/ (standard chess - [elite only](https://database.nikonoel.fr/), puzzles and evaluations).

## Oracle

The are a number of very strong chess engines out there. Will use https://stockfishchess.org/ as an oracle to expand the training dataset and evaluate the model performance.

## Training Goal

Learn an internal representation of winning trajectories in the world of chess (up to N steps). The input of the encoder is the current board configuration (FEN) and up to N moves into the future and N moves into the past. The training process will progresively mask intermediate moves related to the goal and minimize the delta in latent space with the help of a predictor that has knowledge of what was masked (token position).

On top of this encoder trained using the JEPA setup, I intend to then train a decoder to actually play the game. I also want to explore retrograde analysis assisted by this encoder model.

While somewhat specialized to chess, for practical reasons, the technique is very generic in nature and can be scaled to other domains.

## Hardware Setup

Will start by attempting to train this on two 4090s on my home workstation. This may or may not be enough. It really depends on the choice of hyperparameters.

## Why do this work?

To learn about all the different elements of the stack.
