from collections import Counter
from operator import mul, sub
from typing import Tuple

from src.aoc.aoc2024 import YEAR, get_day
from src.aoc.aoc_helper import Aoc


def parse(txt: str) -> tuple[tuple[int, ...], tuple[int, ...]]:
    l, r = list(
        map(
            list,
            zip(*[list(map(int, line.split())) for line in txt.splitlines()]),
        )
    )
    return l, r


def part_a(txt: str) -> int:
    left_col, right_col = parse(txt)
    return sum(
        abs(l - r) for l, r in zip(sorted(sorted(left_col)), sorted(sorted(right_col)))
    )


def part_b(txt: str) -> int:
    l, r = parse(txt)
    return sum(x * r.count(x) for x in l)


def main(txt: str) -> None:
    print("part_a: ", part_a(txt))
    print("part_b: ", part_b(txt))


if __name__ == "__main__":
    aoc = Aoc(day=get_day(), years=YEAR)
    aoc.run(main, submit=True, part="both", readme_update=True)
