# Nine Men's Morris

An AI for Nine Men's Morris, using MiniMax and Deep Q Networks

## Concept

#### Step 1: Develop an opponent using classical algorithms

Our algorithm was created based on the popular and relatively easy to implement "MiniMax" algorithm ([Wikipedia](https://en.wikipedia.org/wiki/Minimax)).

The algorithm works by recursively building a tree of possible future moves with a specified depth (we found that 3 works well; meaning we will look at the next 3 possible moves).
The states the game could be in after 3 moves are then assigned a value estimating good that state is for the player:

- Number of pieces; each piece the player has gives 3 points
- Number of possible moves; each possible move gives 0.1 points
- Number of mills; each mill gives 1 point

That value is calculated for both players and the state is assigned the difference, meaning how much better the player is doing than his opponent.
The algorithm then collapses the tree by assuming that both players play optimally, always trying to maximize the value of the board for them.
By the end, the algorithm then chosses the move with which the best board value can be guaranteed.

#### Step 2: Use that opponent to train an artificial neural network to play the game

Work in progress.

#### Step 3: Further improve the network by letting it play against slightly modified copies of itself

Work in progress.

## Version 1: Completed Step 1

**The Algorithm** created according to Step 1 can be run by executing:
``` shell
python test_human.py
```
To work properly, the GUI has to be enabled in the file `morris.py` using
``` python
GUI = True
```
To let the AI play first, you can skip the players first move in `test_human.py` using
``` python
skip_player = True
```
but make sure it is reset to `False` after the first move.

**Benchmarks** can be performed by running:
``` shell
python test_ai.py
```
The algorithm will compete against a randomly playing opponent.
To save information about time taken to compute moves, logging has to be enabled in `ai.py` using
``` python
LOG = True
```
The logging ooutput will be saved to a file called `log.csv`

The depth the algorithm examines can be changed in the file `ai.py` by changing the line
``` python
depth = 3
```
to use a customized value.
