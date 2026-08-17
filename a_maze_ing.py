#!/usr/bin/env python3

from config import parse, parse_error

import sys
# class Structure:
#     def __init__(self, config_file: str):
#         try:
#             with open(config_file, "r") as f:
#                 settings: list[str] = (f.read()).split("\n")
#             # SPLIT
#             try:
#                 if ("WIDTH" in settings[0]
#                     and "HEIGHT" in settings[1]
#                     and "ENTRY" in settings[2]
#                     and "EXIT" in settings[3]
#                     and "OUTPUT_FILE" in settings[]
#                     and "PERFECT" in settings):
#                     self._width: int = int((settings[0].split("="))[1])
#                     self._heigth: int = int((settings[1].split("="))[1])
#                     x: int = int(((((settings[2].strip(" ")).split("="))[1]).split(","))[0])
#                     y: int = int(((((settings[2].strip(" ")).split("="))[1]).split(","))[1])
#                     self._entry: list[tuple[int, int]] = [x, y]
#                     x: int = int(((((settings[3].strip(" ")).split("="))[1]).split(","))[0])
#                     y: int = int(((((settings[3].strip(" ")).split("="))[1]).split(","))[1])
#                     self._exit: list[tuple[int, int]] = [x, y]
#                     self._output_file: str = (settings[4].strip(" ")).split("=")[1]
#                     self._perfect: bool = False if "false" == (settings[5].strip(" ")).split("=")[1].lower() else True
#                 else:
#                     raise()
#             except:
#                 print("Invalid input in config.txt")
#         except:
#             print("Couldn't open config.txt")
        

def main() -> None:
    try:
        parse(sys.argv[1])
    except parse_error as error:
        print(error)

if __name__ == "__main__":
    main()
