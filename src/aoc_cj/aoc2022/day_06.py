from src.aoc_cj.aoc2022 import YEAR, get_day
from src.aoc_cj.aoc_helper import Aoc


def parser(n: int, txt: str) -> int:
    txt = txt.strip()
    return [i for i in range(n, len(txt)) if len(set(txt[i - n:i])) == n][0]


def part_a(txt: str) -> int:
    return parser(4, txt)


def part_b(txt: str) -> int:
    return parser(14, txt)


def main(txt: str) -> None:
    print("part_a: ", part_a(txt))
    print("part_b: ", part_b(txt))


if __name__ == "__main__":
    aoc = Aoc(day=get_day(), years=YEAR)
    aoc.run(main, submit=True, part='both', readme_update=True)
