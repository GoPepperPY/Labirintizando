#!/usr/bin/env python3

import sys
from config import parse, parse_error
from mazegen.maze_generator import MAZE_GENERATOR
from writer import write_maze, write_error
from menu import loop


def main() -> None:
    """Parse the configuration, generate the maze, save it and show it."""
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} config.txt", file=sys.stderr)
        sys.exit(1)

    try:
        conf = parse(sys.argv[1])
    except parse_error as error:
        print(f"error: {error}", file=sys.stderr)
        sys.exit(1)

    if not conf.seed_provided:
        print(f"no SEED in config, using SEED={conf.seed}")

    gen = MAZE_GENERATOR(
        width=conf.width,
        height=conf.height,
        perfect=conf.perfect,
        entry=conf.entry,
        exit=conf.exit,
        seed=conf.seed
    )
    gen.generate()
    gen.shortest()

    try:
        write_maze(conf.output_file, gen.maze, gen.width, gen.height,
               gen.entry, gen.exit, gen.path_letters())
    except write_error as error:
        print(f"error: {error}", file=sys.stderr)
        sys.exit(1)

    loop(gen)


if __name__ == "__main__":
    main()

