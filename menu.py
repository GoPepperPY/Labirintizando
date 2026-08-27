"""Interactive terminal menu for displaying and regenerating a maze."""

import random

MENU = (
    "=== A-Maze-ing ===\n"
    "1. Re-generate a new maze\n"
    "2. Show / Hide the shortest path\n"
    "3. Rotate the wall colours\n"
    "4. Quit"
)


RESET = "\033[0m"

COLORS = [
    "\033[37m",
    "\033[34m",
    "\033[36m",
    "\033[35m",
    "\033[94m"
]


def show(gen: object, color: str, reset: str) -> None:
    print("\033[2J\033[H", end="")
    gen.generate()
    gen.print_maze(color, reset)
    print(MENU)


def loop(gen: object) -> None:
    color = COLORS[0]
    count = 0
    try:
        show(gen, color, RESET)
    except Exception as e:
        import sys
        print(e)
        sys.exit(1)
    while True:
        try:
            choice = input("Choice? (1-4): ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return
        if choice == "1":
            gen.seed = random.randrange(2**32)
            show(gen, color, RESET)
        elif choice == "2":
            if gen.show_path:
                gen.show_path = False
            else:
                gen.show_path = True
            show(gen, color, RESET)
        elif choice == "3":
            if color == COLORS[0]:
                count += 1
            if color == COLORS[-1]:
                count = 0
            color = COLORS[count]
            count += 1
            show(gen, color, RESET)
        elif choice == "4":
            return
        else:
            print("Please type a number between 1 and 4.")
            continue
