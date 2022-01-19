# Nine Men's Morris

An intelligent board for Nine Men's Morris, using MiniMax and Deep Q Networks controlling a physical board via a Raspberry Pi

## Concept

Our algorithm was created based on the popular and relatively easy to implement "MiniMax" algorithm ([Wikipedia](https://en.wikipedia.org/wiki/Minimax)).

The algorithm works by recursively building a tree of possible future moves with a specified depth (we found that 3 works well; meaning we will look at the next 3 possible moves).
The states the game could be in after 3 moves are then assigned a value estimating good that state is for the player:

- Number of pieces; each piece the player has gives 3 points
- Number of possible moves; each possible move gives 0.1 points
- Number of mills; each mill gives 1 point

That value is calculated for both players and the state is assigned the difference, meaning how much better the player is doing than his opponent.
The algorithm then collapses the tree by assuming that both players play optimally, always trying to maximize the value of the board for them.
By the end, the algorithm then chosses the move with which the best board value can be guaranteed.

## Reasoning Behind Heuristics

Number of pieces:
- This is important to include as the main way to win in Nine Mens Morris is to bring your opponent down to 2 pieces so we want our AI to do whatever is possible to avoid losing. Furthermore, having more pieces gives more opprotunities to make mills.

Number of possible moves:
- When the number of possible moves goes down it is more likely that we could reach a point where we get trapped which would cause the AI to lose. Having a lower number of possible moves could also be correlated to having less pieces which we also want to avoid. Because of these reasons we want to keep the number of possible moves high.

Number of mills:
- The most common way to win is by taking away all but 2 of the opponents pieces and to do that we need mills. It's important that our AI chooses moves that causes them to get mills so it actually wins instead of being at a stalemate just trying to survive.

## Possible Additional Heuristics
- Number of intersections held. Intersections are very beneficial as they give you the most opprotunities to move either blocking a mill from your opponent or making one of your own
- Number of 2 in a row pieces: Before you create a mill often you start with 2 pieces in a row. As we want our AI to win it'd be a good idea to encourage it to make 2 in a row so it can make mills from there.

## Results:

**The Algorithm** can be run by executing:
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
