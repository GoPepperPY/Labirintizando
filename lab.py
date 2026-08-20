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

def open_wall(maze: Maze, cell: Cell, direction: str) -> None:
    dx, dy = DIRECTIONS[direction]
    neighbour = (cell[0] + dx, cell[1] + dy)
    maze[cell][direction] = False
    maze[neighbour][OPPOSITE[direction]] = False

def neighbours(maze: Maze, cell: Cell) -> list[tuple[str, Cell]]:
    found: list[tuple[str, Cell]] = []
    for direction, (dx, dy) in DIRECTIONS.items():
        neighbour = (cell[0] + dx, cell[1] + dy)
        if neighbour in maze:
            found.append((direction, neighbour))
    return found

def carve(maze: Maze, start: Cell, rng: random.Random,
          blocked: set[Cell] | None = None) -> None:
    closed = blocked or set()
    if start not in maze:
        raise ValueError(f"start {start} is outside the maze")
    if start in closed:
        raise ValueError(f"start {start} is a blocked cell")
 
    visited: set[Cell] = {start}
    stack: list[Cell] = [start]
    while stack:
        cell = stack[-1]
        options = [(d, n) for d, n in neighbours(maze, cell)
                   if n not in visited and n not in closed]
        if not options:
            stack.pop()
            continue
        direction, chosen = rng.choice(options)
        open_wall(maze, cell, direction)
        visited.add(chosen)
        stack.append(chosen)
  

def print_maze(maze, x, y):
    for i in range(y):
        print("██", end="")
        for j in range(x):
            if maze[(j, i)]["N"]:
                print("████", end="")
            else:
                print("  ██", end="")
        print("\n██", end="")
        for j in range(x):
            if maze[(j, i)]["E"]:
                print("  ██", end="")
            else:
                print("    ", end="")
        print()
    print("██", end="")
    for _ in range(x):
        print("████", end="")
    print()


if __name__ == "__main__":
    maze: dict[Cell, Walls] = {}
    length = 30
    width = 30
    for i in range(length):
        for j in range(width):
            maze[(j, i)] = {"N":True, "E":True, "S":True, "W":True}
    carve(maze, (0,0), random.Random(1585))
    print_maze(maze, width, length)