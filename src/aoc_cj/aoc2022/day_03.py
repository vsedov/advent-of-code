from src.aoc_cj import solve
from src.aoc_cj.aoc2022 import YEAR, get_day


def part_a(txt: str) -> int:

    return 0


def part_b(txt: str) -> int:

    return 0


def main(txt: str) -> None:
    print(f"part_a: {part_a(txt)}")
    print(f"part_b: {part_b(txt)}")


if __name__ == "__main__":
    from aocd import get_data

    day = get_day()

    solve("template", YEAR, day, get_data(day=day, year=YEAR))
