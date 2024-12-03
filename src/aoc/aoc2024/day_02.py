from itertools import combinations
from pathlib import Path
from typing import TypeAlias

import numpy as np

from src.aoc.aoc2024 import YEAR, get_day
from src.aoc.aoc_helper import Aoc

NDArray: TypeAlias = np.ndarray


def safe(nums: NDArray, /) -> bool:
    diffs = np.diff(nums)
    return np.all((diffs >= 1) & (diffs <= 3)) or np.all((diffs >= -3) & (diffs <= -1))


def part_a(txt: str) -> int:
    return sum(safe(np.fromstring(line, sep=" ")) for line in txt.splitlines())


def part_b(txt: str) -> int:
    return sum(
        safe(nums) or any(map(lambda i: safe(np.delete(nums, i)), range(len(nums))))
        for nums in map(lambda x: np.fromstring(x, sep=" "), txt.splitlines())
    )


def main(txt: str) -> None:
    print(f"part_a: {part_a(txt)}")
    print(f"part_b: {part_b(txt)}")


if __name__ == "__main__":
    aoc = Aoc(day=get_day(), years=YEAR)
    aoc.run(main, submit=True, part="both", readme_update=True)

# def part_a(txt: str) -> int:
#     return sum(
#         safe(np.array([int(n) for n in line.split()])) for line in txt.splitlines()
#     )
#
#
# def part_b(txt: str) -> int:
#     return sum(
#         safe(nums := np.array([int(n) for n in line.split()]))
#         or any(safe(np.delete(nums, i)) for i in range(len(nums)))
#         for line in txt.splitlines()
#     )
