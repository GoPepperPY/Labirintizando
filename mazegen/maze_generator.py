import random
from collections import deque
import sys


class MAZE_GENERATOR():
    def __init__(self, width: int,
                 height: int, entry: tuple[int, int],
                 exit: tuple[int, int], perfect: bool, seed: int):
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.seed = seed
        self.show_path: bool = False
        self.maze: dict[tuple[int, int], dict[str, bool]] = {}
        self.visited: set[tuple] = set()
        self.chance: float = 0.10
        self.cells_42: set[tuple] = set()
        self.path: list[tuple]

    def create_closed(self) -> None:
        for i in range(self.height):
            for j in range(self.width):
                self.maze[(j, i)] = {"N": True, "E": True, "S": True, "W": True}

    def print_maze(self, color: str, reset: str) -> None:
        print(self.exit)
        for i in range(self.height):
            print(f"{color}██{reset}", end="")
            for j in range(self.width):
                if self.maze[j, i]["N"]:
                    print(f"{color}████{reset}", end="")
                else:
                    print(f"{color}  ██{reset}", end="")
            print(f"{color}\n██{reset}", end="")
            for j in range(self.width):
                if (j, i) in self.path and self.exit != (j, i) != self.entry:
                    if self.maze[j, i]["E"]:
                        print("\033[33m██\033[0m"+f"{color}██{reset}", end="")
                    else:
                        print("\033[33m██\033[0m"+"  ", end="")
                elif (j, i) == self.entry:
                    if self.maze[j, i]["E"]:
                        print("\033[32m██\033[0m"+f"{color}██{reset}", end="")
                    else:
                        print("\033[32m██\033[0m"+"  ", end="")
                elif (j, i) == self.exit:
                    if self.maze[j, i]["E"]:
                        print("\033[31m██\033[0m"+f"{color}██{reset}", end="")
                    else:
                        print("\033[31m██\033[0m"+"  ", end="")
                elif all(self.maze[j, i].values()):
                    print("\033[32m██\033[0m"+f"{color}██{reset}", end="")
                elif self.maze[j, i]["E"]:
                    print(f"{color}  ██{reset}", end="")
                else:
                    print(f"{color}    {reset}", end="")
            print()
        print(f"{color}██{reset}", end="")
        for _ in range(self.width):
            print(f"{color}████{reset}", end="")
        print()

    def possible_moves(self, cell: tuple) -> list[tuple]:
        x, y = cell
        candidates = [
            (x, y - 1),
            (x, y + 1),
            (x + 1, y),
            (x - 1, y),
        ]
        moves = []
        for coord in candidates:
            if coord in self.maze and coord not in self.visited:
                moves.append(coord)
        return moves

    def break_wall(self, cell: tuple, move: tuple) -> None:
        dc = cell[0] - move[0]
        dl = cell[1] - move[1]

        if dl == 1:
            self.maze[move]["S"] = False
            self.maze[cell]["N"] = False
        elif dl == -1:
            self.maze[move]["N"] = False
            self.maze[cell]["S"] = False
        elif dc == 1:
            self.maze[move]["E"] = False
            self.maze[cell]["W"] = False
        elif dc == -1:
            self.maze[move]["W"] = False
            self.maze[cell]["E"] = False

    def define_42(self) -> None:
        center = (self.width // 2, self.height // 2)
        cells_42 = [
            (-3, -2), (-3, -1), (-3, 0), (-2, 0), (-1, 0), (-1, 1),
            (-1, 2), (1, -2), (2, -2), (3, -2), (3, -1), (1, 0), (2, 0),
            (3, 0), (1, 1), (1, 2), (2, 2), (3, 2)
        ]
        if self.width < 9 or self.height < 7:
            return
        self.cells_42.update(set((center[0] + cell[0], center[1] + cell[1]) for cell in cells_42))
        if self.entry in self.cells_42 or self.exit in self.cells_42:
            raise Exception("Entry and Exit coordinates "
                            "must be different than 42 cells")
        self.visited.update(self.cells_42)

    def cave_imperfect(self) -> None:
        for cell, walls in self.maze.items():
            column, line = cell
            vizinhos = {
                "N": (column, line - 1),
                "S": (column, line + 1),
                "E": (column + 1, line),
                "W": (column - 1, line),
            }
            for direcao, vizinho in vizinhos.items():
                if (
                    cell not in self.cells_42
                    and vizinho not in self.cells_42
                    and vizinho in self.maze
                    and walls[direcao]
                    and random.random() < self.chance
                ):
                    self.break_wall(cell, vizinho)

    def cave_perfect(self, cell: tuple[int, int]) -> None:
        self.visited.add(cell)
        moves = self.possible_moves(cell)
        random.shuffle(moves)
        for move in moves:
            if move not in self.visited:
                self.break_wall(cell, move)
                self.cave_perfect(move)

    def shortest(self) -> None:
        queue = deque([self.entry])
        veio_de = {self.entry: None}
        direcoes = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0)}
        while queue:
            atual = queue.popleft()
            if atual == self.exit:
                break
            for direcao, (dx, dy) in direcoes.items():
                if not self.maze[atual][direcao]:
                    vizinho = (atual[0] + dx, atual[1] + dy)
                    if vizinho not in veio_de:
                        veio_de[vizinho] = atual
                        queue.append(vizinho)
        passo = self.exit
        while passo is not None:
            self.path.append(passo)
            passo = veio_de[passo]
        self.path.reverse()

    def generate(self) -> None:
        random.seed(self.seed)
        self.path = []
        self.visited = set()
        self.create_closed()
        self.define_42()
        self.cave_perfect(self.entry)
        if not self.perfect:
            self.cave_imperfect()
        if self.show_path:
            self.shortest()
