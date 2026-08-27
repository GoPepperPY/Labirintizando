"""Interactive terminal menu for displaying and regenerating a maze."""



MENU = (
    "=== A-Maze-ing ===\n"
    "1. Re-generate a new maze\n"
    "2. Show / Hide the shortest path\n"
    "3. Rotate the wall colours\n"
    "4. Quit"
)


def show(gen: object, show_path: bool, colour: int) -> None:
    print("\033[2J\033[H", end="")
    gen.generate()
    gen.print_maze()
    print(MENU)


def loop(gen: object) -> None:
    show_path = False
    colour = 0
    while True:
        try:
            choice = input("Choice? (1-4): ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return
        if choice == "1":
            show(gen, show_path, colour)
        elif choice == "2":
            show_path = not show_path
        elif choice == "3":
            pass
        elif choice == "4":
            return
        else:
            print("Please type a number between 1 and 4.")
            continue
