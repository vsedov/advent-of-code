from itertools import combinations
from pathlib import Path
from typing import TypeAlias

import numpy as np
from numba import njit

from src.aoc.aoc2024 import YEAR, get_day
from src.aoc.aoc_helper import Aoc

NDArray: TypeAlias = np.ndarray


@njit
def check_sequence(nums: np.ndarray) -> bool:
    if len(nums) <= 1:
        return True

    diffs = np.diff(nums)
    return np.all((diffs >= 1) & (diffs <= 3)) or np.all((diffs >= -3) & (diffs <= -1))


@njit
def check_removable(nums: np.ndarray) -> bool:
    n = len(nums)
    for i in range(n):
        # check sequence validitity by eval adjacent val - skip ith
        valid = True
        for j in range(n - 1):
            if j < i - 1:
                diff = nums[j + 1] - nums[j]
            elif j == i - 1:
                if i < n - 1:
                    diff = nums[i + 1] - nums[j]
                else:
                    continue
            else:
                diff = nums[j + 2] - nums[j + 1]

            if not (
                1 <= abs(diff) <= 3
                and ((diff > 0 and diff <= 3) or (diff < 0 and diff >= -3))
            ):
                valid = False
                break

        if valid:
            return True
    return False


def part_a(txt: str) -> int:
    return sum(
        check_sequence(np.fromstring(line, sep=" ")) for line in txt.splitlines()
    )


def part_b(txt: str) -> int:
    return sum(
        check_sequence(np.fromstring(line, sep=" "))
        or check_removable(np.fromstring(line, sep=" "))
        for line in txt.splitlines()
    )


def main(txt: str) -> None:
    print(f"part_a: {part_a(txt)}")
    print(f"part_b: {part_b(txt)}")


if __name__ == "__main__":
    aoc = Aoc(day=get_day(), years=YEAR)
    aoc.run(main, submit=True, part="both", readme_update=True)
