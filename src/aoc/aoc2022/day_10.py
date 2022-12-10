from typing import Tuple

from src.aoc.aoc2022 import YEAR, get_day
from src.aoc.aoc_helper import Aoc


def parse(txt: str) -> Tuple[int, int]:
    cycles = 0
    x_reg = 1

    for i, line in enumerate(txt.split(), start=1):
        cycles += i * x_reg if i % 40 == 20 else 0
        x_reg += int(line) if any(c.isdigit() for c in line) else 0

    return cycles, x_reg


def part_a(txt: str) -> int:
    return parse(txt)[0]


def part_b(txt: str) -> int:
    cycles, x_reg = parse(txt)


def main(txt: str) -> None:
    print("part_a: ", part_a(txt))
    print("part_b: ", part_b(txt))


if __name__ == "__main__":
    aoc = Aoc(day=get_day(), years=YEAR)
    aoc.run(main, submit=True, part='a', readme_update=False)
