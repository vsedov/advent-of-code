from typing import Generator

from src.aoc_cj.aoc2022 import YEAR, get_day
from src.aoc_cj.aoc_helper import Aoc


def get_calories(txt: str) -> Generator[int, None, None]:
    return (sum(map(int, x.split())) for x in txt.split("\n\n"))


def part_a(txt: str) -> int:
    return max(get_calories(txt))


def part_b(txt: str) -> int:
    return sum(sorted(get_calories(txt), reverse=True)[:3])


def main(txt: str) -> None:
    print(f"part_a: {part_a(txt)}")
    print(f"part_b: {part_b(txt)}")


if __name__ == "__main__":
    aoc = Aoc(day=get_day(), years=YEAR)
    aoc.run(main, submit=True, part="both")
