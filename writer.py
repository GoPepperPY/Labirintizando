class write_error(Exception):
    """Raised when the maze cannot be written to the output file."""

    def __init__(self, message: str = "") -> None:
        super().__init__(message)


def write_maze(path: str, maze: list[list[int]],
               entry: tuple[int, int], exit_cell: tuple[int, int],
               shortest_path: str) -> None:
    """Write the maze grid, the entry, the exit and the solution."""

    lines: list[str] = []
    for row in maze:
        lines.append("".join(f"{cell:x}" for cell in row))
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
