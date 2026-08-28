_This project has been created as part of the 42 curriculum by gopiment, danicamp._

# A-Maze-ing

## Description

A-Maze-ing is a maze generator written in Python. It reads a configuration
file, generates a maze in one of two modes, writes it to a file using a
hexadecimal wall encoding, and displays it in the terminal with an
interactive menu.

Two generation modes are supported:

- **Perfect** (`PERFECT=True`): a single path exists between any two cells,
  so there is exactly one route from the entry to the exit.
- **Playable** (`PERFECT=False`, the default): the board keeps several
  independent routes (loops) so it can be used by a Pac-Man-like game.

Every generated maze contains a visible "42" pattern drawn with fully closed
cells, and a shortest path from the entry to the exit is always computed.

## Instructions

Run the program with a configuration file:

```
python3 a_maze_ing.py config.txt
```

Or use the Makefile:

```
make install    # install flake8 and mypy
make run        # run with config.txt
make lint       # run flake8 and mypy
make clean      # remove caches and build artifacts
```

### Interactive menu

Once the maze is displayed, the following options are available:

1. Re-generate a new maze
2. Show / Hide the shortest path
3. Rotate the wall colours
4. Quit

## Configuration file format

One `KEY=VALUE` pair per line. Lines starting with `#` are comments and are
ignored. Keys are case-insensitive.

| Key           | Description                       | Example                |
|---------------|-----------------------------------|------------------------|
| `WIDTH`       | Maze width in cells               | `WIDTH=15`             |
| `HEIGHT`      | Maze height in cells              | `HEIGHT=15`            |
| `ENTRY`       | Entry coordinates (x,y)           | `ENTRY=0,0`            |
| `EXIT`        | Exit coordinates (x,y)            | `EXIT=14,14`           |
| `OUTPUT_FILE` | Output filename                   | `OUTPUT_FILE=maze.txt` |
| `PERFECT`     | Perfect maze or playable board    | `PERFECT=False`        |
| `SEED`        | Optional seed for reproducibility | `SEED=42`              |

If `SEED` is omitted, a random seed is generated and printed so the maze can
be reproduced.

## Output file format

One hexadecimal digit per cell, one row per line. Each digit encodes the
closed walls of a cell: north is bit 0 (value 1), east bit 1 (value 2),
south bit 2 (value 4), west bit 3 (value 8). A closed wall sets the bit to 1.

After an empty line, three lines follow: the entry coordinates, the exit
coordinates, and the shortest path as a string of `N`, `E`, `S`, `W` letters.

## Maze generation algorithm

The perfect maze is carved with an **iterative depth-first backtracker**: the
walk digs as deep as possible, then backtracks when it reaches a cell with no
unvisited neighbour. Because each cell is visited exactly once, the result is
a spanning tree with a single route between any two cells.

For the playable board, extra passages are opened to create loops, so the
board keeps several independent routes.

The shortest path from entry to exit is found with a **breadth-first search**,
which visits each cell once and is therefore efficient even when the maze
contains loops.

### Why these algorithms

The backtracker is simple, fast, and produces long winding corridors that
look like a proper maze. BFS is the natural choice for the shortest path
because the first time it reaches a cell is always by the shortest route.

## Reusable module

The generation logic lives in the `mazegen` package, installable with pip:

```
pip install mazegen-1.0.0-py3-none-any.whl
```

Basic usage:

```python
from mazegen import MAZE_GENERATOR

gen = MAZE_GENERATOR(
    width=15,
    height=15,
    entry=(0, 0),
    exit=(14, 14),
    perfect=False,
    seed=42,
)
gen.generate()

structure = gen.maze          # dict[(x, y) -> {"N": bool, "E": ...}]
solution = gen.path_letters()  # e.g. "SESEES..."
```

The package is built from source with:

```
pip install build
python -m build
```

## Resources

- Maze generation algorithms: https://en.wikipedia.org/wiki/Maze_generation_algorithm
- Breadth-first search: https://en.wikipedia.org/wiki/Breadth-first_search
- Spanning trees: https://en.wikipedia.org/wiki/Spanning_tree

### Use of AI

AI was used as a helper for explaining concepts (BFS, backtracking, bitwise
wall encoding) and reviewing error handling in the configuration parser. All generated code was
reviewed, tested, and adapted by the team.

## Team and project management

- **gopiment**: parsing/validation
- **danicamp**: mazegen/visualizer

<!-- Fill in: planning and how it evolved, what worked well, what could be
     improved, and any specific tools used. -->
