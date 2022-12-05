from src.aoc_cj.aoc2022 import YEAR, get_day
from src.aoc_cj.aoc_helper import Aoc


def part_a(txt: str) -> int:

    return 0


def part_b(txt: str) -> int:

    return 0


def main(txt: str) -> None:
    print("part_a: ", part_a(txt))
    print("part_b: ", part_b(txt))


if __name__ == "__main__":
    aoc = Aoc(day=get_day(), years=YEAR)
    aoc.run(main, submit=False, part='a', readme_update=False)
