from collections import defaultdict
from itertools import product
from typing import Set, Tuple

import more_itertools as mi
import numpy as np
import numpy.typing as npt
from numba import jit, njit
from numba.typed import List

from src.aoc.aoc2024 import YEAR, get_day
from src.aoc.aoc_helper import Aoc


class foo(Exception):
    pass


def explore(mapping: dict[complex, str], start: complex) -> set[complex]:
    pos, heading = start, -1j
    seen = set()

    grid = defaultdict(lambda: None, mapping)

    while pos in mapping:
        if (pos, heading) in seen:
            raise foo
        seen.add((pos, heading))
        next_pos = pos + heading
        if grid[next_pos] == "#":
            heading *= 1j
            next_pos = pos
        pos = next_pos
    return {p for p, _ in seen}


def parse_map(txt: str) -> tuple[dict[complex, str], complex]:
    # Vectorized parsing using numpy
    grid = np.array([list(line) for line in txt.splitlines()])
    rows, cols = grid.shape

    y, x = np.where(grid == "^")
    start = complex(x[0], y[0])

    mapping = {complex(x, y): grid[y, x] for y, x in product(range(rows), range(cols))}

    return mapping, start


def part_a(txt: str) -> int:
    mapping, start = parse_map(txt)
    return len(explore(mapping, start))


def part_b(txt: str) -> int:
    mapping, start = parse_map(txt)
    path = explore(mapping, start)

    path_set = set(path)
    causes_loop = set()

    base_mapping = defaultdict(lambda: None, mapping)

    for pos in path_set:
        base_mapping[pos] = "#"
        try:
            explore(base_mapping, start)
        except foo:
            causes_loop.add(pos)
        base_mapping[pos] = mapping[pos]  # Restore original value

    return len(causes_loop)


def main(txt: str) -> None:
    print("part_a: ", part_a(txt))
    print("part_b: ", part_b(txt))


if __name__ == "__main__":
    aoc = Aoc(day=get_day(), years=YEAR)
    aoc.run(main, submit=False, part="both", readme_update=True, profile=True)
