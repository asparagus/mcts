# MCTS
Repository for developing Monte Carlo Tree Search algorithms

Currently have a tic-tac-toe and connect-four games implemented.

## Experimentation
The algorithms can be tried by running a "Tournament".

```
usage: tournament.py [-h] [--n N] a b

Script for running a competition between agents.

positional arguments:
  game        Game, one of "tic_tac_toe", "connect_four"
  a           Competitor, one of "human", "random", "mcts"
  b           Competitor, one of "human", "random", "mcts"
```

From the main directory, this can be run using `python -m mcts.tournament`.

Example run and output:
```
$ python -m mcts.tournament connect_four mcts random --n=10
Namespace(a='mcts', b='random', n=10)
0: 1, 0
1: 1, 0
2: 1, 0
3: 1, 0
4: 1, 0
5: 1, 0
6: 1, 0
7: 0, 1
8: 1, 0
9: 1, 0
Tournament results: 0.9 / 0.1
```

## Testing
Test using pytest:
```
python -m pytest
```
