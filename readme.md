# Snake-in-the-box two-players game

An implementation of the two-player version of the 'Snake in the box' problem.
Create your own strategy in the strategy.py file!

## Rules

- The game is played on an undirected graph (randomly generated or preset)
- Each player starts on a vertex of the graph (randomly chosen or preset
- At each turn, the player chooses a vertex adjacent to their snake's head to grow the snake,
while following the rules:
  - the new vertex must not be occupied by either snake
  - each vertex of a snake must have at most two adjacent vertices belonging to a snake.
- The game ends when a player cannot move anymore. The first player that cannot move loses.

## Run the game

```
$ python main.py -h

usage: main.py [-h] [--graph {erdos,cube}] [--n N] [--p P] [--d D] [--s0 S0] [--s1 S1] [--seed SEED] [--verbose] [--ui]

Snake-in-the-Box Game Runner

options:
  -h, --help            show this help message and exit
  --graph {erdos,cube}  Graph type
  --n N                 Graph size (Erdos-Renyi)
  --p P                 Edge probability (Erdos-Renyi)
  --d D                 Dimension for hypercube
  --s0 S0               Strategy for player 0
  --s1 S1               Strategy for player 1
  --seed SEED           Random seed for start positions
  --verbose             Print moves
  --ui                  Run using the graphical UI. Incompatible with --verbose.
```

## Implementing a new strategy

1. Extend the Strategy class in strategy.py
2. Implement the select_move method
3. Add the new strategy to the `STRATEGIES` dictionary at the end ot the `strategies.py` file
4. Run the game with the new strategy!
