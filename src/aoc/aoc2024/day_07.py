from typing import Tuple

import numpy as np
from numba import njit, prange
from numba.typed import Dict
from numba.typed import List as NumbaList

from src.aoc.aoc2024 import YEAR, get_day
from src.aoc.aoc_helper import Aoc

from collections.abc import Generator, Sequence


def parse(txt: str) -> Generator[tuple[int, tuple[int, ...]], None, None]:
    for line in txt.splitlines():
        target, sep, nums = line.partition(": ")
        assert sep == ": "
        yield int(target), tuple(map(int, nums.split()))


def _possible_results(nums: Sequence[int], *, concat_op: bool = False) -> Generator[int, None, None]:
    if len(nums) == 1:
        yield nums[0]
        return
    *rest, last = nums
    for r in _possible_results(rest, concat_op=concat_op):
        yield r + last
        yield r * last
        if concat_op:
            yield int(str(r) + str(last))


def solve(txt: str, *, concat_op: bool = False) -> int:
    return sum(target for target, nums in parse(txt) if target in _possible_results(nums, concat_op=concat_op))


def part_a(txt: str) -> int:
    return solve(txt)


def part_b(txt: str) -> int:
    return solve(txt, concat_op=True)


def main(txt: str) -> None:
    print("part_a: ", part_a(txt))
    print("part_b: ", part_b(txt))


if __name__ == "__main__":
    aoc = Aoc(day=get_day(), years=YEAR)
    aoc.run(main, submit=False, part="both", readme_update=True, profile=True)
