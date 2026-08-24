#!/usr/bin/env python3
"""Carving passages and stamping the '42' pattern into a maze."""

import random

Cell = tuple[int, int]
Walls = dict[str, bool]
Maze = dict[Cell, Walls]

DIRECTIONS: dict[str, tuple[int, int]] = {
    "N": (0, -1),
    "E": (1, 0),
    "S": (0, 1),
    "W": (-1, 0),
}

OPPOSITE: dict[str, str] = {"N": "S", "E": "W", "S": "N", "W": "E"}

GLYPH: tuple[str, ...] = (
    "#...###",
    "#.....#",
    "###.###",
    "..#.#..",
    "..#.###",
)


def build_closed(width: int, height: int) -> Maze:
    """Return a maze of the given size with every wall closed."""

    maze: Maze = {}
    for y in range(height):
        for x in range(width):
            maze[(x, y)] = {"N": True, "E": True, "S": True, "W": True}
    return maze


def glyph_cells(width: int, height: int, reserved: set[Cell]) -> set[Cell]:
    """Return the cells that must stay closed to draw a '42'."""

    length_42 = len(GLYPH)
    width_42 = len(GLYPH[0])
    if width_42 + 2 > width or length_42 + 2 > height:
        print("warning: maze too small to draw the '42' pattern")
        return set()
    base_x = (width - width_42) // 2
    base_y = (height - length_42) // 2
    for shift_x, shift_y in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
        left = base_x + shift_x
        top = base_y + shift_y
        if not (1 <= left and left + width_42 <= width - 1):
            continue
        if not (1 <= top and top + length_42 <= height - 1):
            continue
        cells: set[Cell] = set()
        for y, row in enumerate(GLYPH):
            for x, mark in enumerate(row):
                if mark == "#":
                    cells.add((left + x, top + y))
        if not cells & reserved:
            return cells
    print("warning: no room to draw the '42' pattern")
    return set()


def open_wall(maze: Maze, cell: Cell, direction: str) -> None:
    """Open one wall on both sides so the two cells stay coherent."""

    dx, dy = DIRECTIONS[direction]
    neighbour = (cell[0] + dx, cell[1] + dy)
    maze[cell][direction] = False
    maze[neighbour][OPPOSITE[direction]] = False


def neighbours(maze: Maze, cell: Cell) -> list[tuple[str, Cell]]:
    """Return the in-bounds neighbours of a cell."""

    found: list[tuple[str, Cell]] = []
    for direction, (dx, dy) in DIRECTIONS.items():
        neighbour = (cell[0] + dx, cell[1] + dy)
        if neighbour in maze:
            found.append((direction, neighbour))
    return found


def carve(maze: Maze, start: Cell, rng: random.Random,
          blocked: set[Cell]) -> None:
    """Carve a spanning tree of passages with an iterative backtracker."""

    if start not in maze:
        raise ValueError(f"start {start} is outside the maze")
    if start in blocked:
        raise ValueError(f"start {start} is a blocked cell")
    visited: set[Cell] = {start}
    stack: list[Cell] = [start]
    while stack:
        cell = stack[-1]
        options = [(d, n) for d, n in neighbours(maze, cell)
                   if n not in visited and n not in blocked]
        if not options:
            stack.pop()
            continue
        direction, chosen = rng.choice(options)
        open_wall(maze, cell, direction)
        visited.add(chosen)
        stack.append(chosen)


def print_maze(maze: Maze, width: int, height: int,
               blocked: set[Cell]) -> None:
    """Draw the maze in the terminal using solid blocks."""

    for y in range(height):
        print("██", end="")
        for x in range(width):
            print("████" if maze[(x, y)]["N"] else "  ██", end="")
        print("\n██", end="")
        for x in range(width):
            print("░░" if (x, y) in blocked else "  ", end="")
            print("██" if maze[(x, y)]["E"] else "  ", end="")
        print()
    print("██" * (width * 2 + 1))


if __name__ == "__main__":
    WIDTH = 21
    HEIGHT = 21
    ENTRY = (0, 0)
    EXIT = (WIDTH - 1, HEIGHT - 1)

    board = build_closed(WIDTH, HEIGHT)
    pattern = glyph_cells(WIDTH, HEIGHT, {ENTRY, EXIT})
    carve(board, ENTRY, random.Random(1585), pattern)
    print_maze(board, WIDTH, HEIGHT, pattern)
