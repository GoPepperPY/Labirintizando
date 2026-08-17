#!/usr/bin/env python3

import sys

from config import parse, parse_error
from mazegen.mazegenerator import MazeGenerator
from writer import write_maze, write_error

def main() -> None:
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} config.txt")
        sys.exit(1)
    try:
        conf = parse(sys.argv[1])
    except parse_error as error:
        print(f"error: {error}")
        sys.exit(1)

    gen = MazeGenerator(
        size=(conf.width, conf.height),
        perfect=conf.perfect,
        entry_cell=conf.entry,
        exit_cell=conf.exit,
        seed=conf.seed,
    )

    if gen.shortest_path is False:
        print("error: no path from entry to exit")
        sys.exit(1)

    try:
        write_maze(conf.output_file, gen.maze, gen.maze_entry,
                   gen.maze_exit, str(gen.shortest_path))
    except write_error as error:
        print(f"error: {error}")
        sys.exit(1)

if __name__ == "__main__":
    main()