from collections.abc import Iterable
from itertools import pairwise
from typing import TypeAlias

from src.aoc.aoc2024 import YEAR, get_day
from src.aoc.aoc_helper import Aoc

Nums: TypeAlias = Iterable[int]


def safe(nums: Nums, /) -> bool:
    match [b - a for a, b in pairwise(nums)]:
        case [*diffs] if all(d in {1, 2, 3} for d in diffs) or all(
            d in {-1, -2, -3} for d in diffs
        ):
            return True
        case _:
            return False


def part_a(txt: str) -> int:
    return sum(safe(map(int, nums)) for nums in map(str.split, txt.splitlines()))


def part_b(txt: str) -> int:
    return sum(
        safe(nums := list(map(int, line.split())))
        or any(safe(nums[:i] + nums[i + 1 :]) for i in range(len(nums)))
        for line in txt.splitlines()
    )


def main(txt: str) -> None:
    print("part_a: ", part_a(txt))
    print("part_b: ", part_b(txt))


if __name__ == "__main__":
    aoc = Aoc(day=get_day(), years=YEAR)
    aoc.run(main, submit=True, part="both", readme_update=True)
