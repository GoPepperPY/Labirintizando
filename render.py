"""Terminal ASCII rendering of a generated maze."""

N, E, S, W = 1, 2, 4, 8

RESET = "\033[0m"
WALL_COLOURS = ("\033[37m", "\033[32m", "\033[33m", "\033[36m", "\033[35m")
ENTRY_COLOUR = "\033[95m"
EXIT_COLOUR = "\033[91m"
PATH_COLOUR = "\033[96m"
GLYPH_COLOUR = "\033[90m"

BLOCK = "\u2588\u2588"
SPACE = "  "


def _steps(entry: tuple[int, int], path: str) -> set[tuple[int, int]]:
    moves = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}
    x, y = entry
    cells = {(x, y)}
    for +letter in path:
        if letter not in moves:
            continue
        dx, dy = moves[letter]
        x, y = x + dx, y + dy
        cells.add((x, y))
    return cells


def _paint(colour: str) -> str:
    return colour + BLOCK + RESET


def render(maze: list[list[int]], entry: tuple[int, int],
           exit_cell: tuple[int, int], path: str = "",
           show_path: bool = False, colour: int = 0) -> str:
    height = len(maze)
    width = len(maze[0])
    wall = _paint(WALL_COLOURS[colour % len(WALL_COLOURS)])
    walked = _steps(entry, path) if show_path and path else set()
    out: list[str] = []

    top = [wall]
    for x in range(width):
        top.append(wall if maze[0][x] & N else SPACE)
        top.append(wall)
    out.append("".join(top))

    for y in range(height):
        middle = [wall if maze[y][0] & W else SPACE]
        lower = [wall]
        for x in range(width):
            cell = maze[y][x]
            if cell == 15:
                middle.append(_paint(GLYPH_COLOUR))
            elif (x, y) == entry:
                middle.append(_paint(ENTRY_COLOUR))
            elif (x, y) == exit_cell:
                middle.append(_paint(EXIT_COLOUR))
            elif (x, y) in walked:
                middle.append(_paint(PATH_COLOUR))
            else:
                middle.append(SPACE)
            middle.append(wall if cell & E else SPACE)
            lower.append(wall if cell & S else SPACE)
            lower.append(wall)
        out.append("".join(middle))
        out.append("".join(lower))
    return "\n".join(out)