"""Writing the generated maze to the output file."""

BITS: dict[str, int] = {"N": 1, "E": 2, "S": 4, "W": 8}

Cell = tuple[int, int]
Maze = dict[Cell, dict[str, bool]]


class write_error(Exception):
    """Raised when the maze cannot be written to the output file."""

    def __init__(self, message: str = "") -> None:
        """Store the message describing what went wrong.

        Args:
            message: Human-readable description of the problem.
        """
        super().__init__(message)


def to_hex(maze: Maze, width: int, height: int) -> list[str]:
    """Return the maze as one hexadecimal digit per cell, row by row."""

    rows: list[str] = []
    for y in range(height):
        row = ""
        for x in range(width):
            try:
                walls = maze[(x, y)]
            except KeyError as error:
                raise write_error(f"cell {x},{y} is missing") from error
            value = 0
            for direction, bit in BITS.items():
                if walls[direction]:
                    value |= bit
            row += f"{value:x}"
        rows.append(row)
    return rows


def write_maze(path: str, maze: Maze, width: int, height: int,
               entry: Cell, exit_cell: Cell,
               shortest_path: str) -> None:
    """Write the maze grid, the entry, the exit and the solution."""

    lines: list[str] = to_hex(maze, width, height)
    lines.append("")
    lines.append(f"{entry[0]},{entry[1]}")
    lines.append(f"{exit_cell[0]},{exit_cell[1]}")
    lines.append(shortest_path)
    try:
        with open(path, "w", encoding="utf-8") as f:
            for line in lines:
                f.write(f"{line}\n")
    except OSError as error:
        raise write_error(f"cannot write {path}: "
                          f"{error.strerror}") from error
