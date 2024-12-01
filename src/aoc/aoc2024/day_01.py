from collections import Counter
from operator import mul, sub
from typing import Tuple

from src.aoc.aoc2024 import YEAR, get_day
from src.aoc.aoc_helper import Aoc


def parse(txt: str) -> Tuple[Tuple[int, ...], Tuple[int, ...]]:
    cols = tuple(zip(*(map(int, line.split()) for line in txt.splitlines())))
    if len(cols) != 2:
        raise ValueError("Input must yield exactly two columns")
    return cols


def part_a(txt: str) -> int:
    left, right = parse(txt)
    return sum(map(abs, map(sub, sorted(left), sorted(right))))


def part_b(txt: str) -> int:
    left, right = parse(txt)
    return sum(l * count for l, count in zip(left, Counter(right).values()))


def main(txt: str) -> None:
    print("part_a: ", part_a(txt))
    print("part_b: ", part_b(txt))


if __name__ == "__main__":
    aoc = Aoc(day=get_day(), years=YEAR)
    aoc.run(main, submit=True, part="both", readme_update=True)
