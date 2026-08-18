#!/usr/bin/env python3

import random


class parse_error(Exception):
    """Raised when the configuration file is missing or invalid."""

    def __init__(self, message: str = "") -> None:
        super().__init__(message)


REQUIRED_KEYS = ("WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT")


def _as_coords(pairs: dict[str, str], key: str) -> tuple[int, int]:
    """Return the value of `key` as an (x, y) pair of integers."""

    parts: list[str] = pairs[key].split(",")
    if len(parts) != 2:
        raise parse_error(f"{key}: expected x,y, got {pairs[key]}")
    try:
        return (int(parts[0]), int(parts[1]))
    except ValueError:
        raise parse_error(f"{key}: expected two integers, got {pairs[key]}")


class parse:
    """Validated maze settings read from a KEY=VALUE text file."""

    def __init__(self, path: str) -> None:
        pairs = self._read_pairs(path)
        self._extract(pairs)
        self._validate()

    def _validate(self) -> None:
        """Check the extracted values describe a maze that can be built."""

        if self.width < 2 or self.height < 2:
            raise parse_error(
                "maze must be at least 2x2 cells, "
                f"got {self.width}x{self.height}"
            )
        x, y = self.entry
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise parse_error(
                f"{x},{y} is outside the "
                f"{self.width}x{self.height} maze"
            )
        x, y = self.exit
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise parse_error(
                f"{x},{y} is outside the "
                f"{self.width}x{self.height} maze"
            )
        if self.entry == self.exit:
            raise parse_error("ENTRY and EXIT must be different cells")

    def _extract(self, pairs: dict[str, str]) -> None:
        """ Convert the raw string values into typed attributes. """

        missing = [key for key in REQUIRED_KEYS if key not in pairs]
        if missing:
            raise parse_error(f"missing key(s): {', '.join(missing)}")
        try:
            self.width: int = int(pairs["WIDTH"])
            self.height: int = int(pairs["HEIGHT"])
            self.entry: tuple[int, int] = _as_coords(pairs, "ENTRY")
            self.exit: tuple[int, int] = _as_coords(pairs, "EXIT")
            self.output_file: str = pairs["OUTPUT_FILE"]
            self.perfect: bool = (True if pairs["PERFECT"].lower() == "true"
                                  else False)
            self.seed_provided: bool = True if "SEED" in pairs else False
            self.seed: int = (random.randrange(2**32) if "SEED" not in pairs
                              else int(pairs["SEED"]))

        except ValueError as error:
            raise parse_error(str(error))

    def _read_pairs(self, path: str) -> dict[str, str]:
        """Parse KEY=VALUE lines, ignoring comments and blank lines."""

        try:
            with open(path, "r") as f:
                lines: list[str] = (f.read()).splitlines()

        except OSError as error:
            raise parse_error(f"cannot read {path}: "
                              f"{error.strerror}")

        pairs: dict[str, str] = {}
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                raise parse_error(f"expected KEY=VALUE, got {line}")
            key, value = line.split("=", 1)
            key = (key.strip()).upper()
            value = value.strip()
            if not key:
                raise parse_error(f"empty key in {line}")
            if not value:
                raise parse_error(f"empty value for {key}")
            if key in pairs:
                raise parse_error(f"duplicate key {key}")
            pairs[key] = value
        return pairs
