from collections import Counter
from functools import reduce
from typing import Tuple

from src.aoc.aoc2022 import YEAR, get_day
from src.aoc.aoc_helper import Aoc


def convert_char(chr: str) -> int:

    return ord(chr.lower()) - ord("a") + (1 if chr.islower() else 27)


def split_data(data: str) -> Tuple[str, str]:
    half = len(data) // 2
    return data[:half], data[half:]


def check_duplicates(*strings: str) -> int:

    set_conditions = reduce(lambda x, y: x.intersection(y), [set(Counter(i).keys()) for i in strings])
    return convert_char(set_conditions.pop())


def part_a(txt: str) -> int:

    return sum(check_duplicates(*split_data(i)) for i in txt.splitlines())


def part_b(txt: str) -> int:

    return sum(check_duplicates(*txt.splitlines()[i:i + 3]) for i in range(0, len(txt.splitlines()), 3))


def main(txt: str) -> None:
    print(f"part_a: {part_a(txt)}")
    print(f"part_b: {part_b(txt)}")


if __name__ == "__main__":
    aoc = Aoc(day=get_day(), years=YEAR)
    aoc.run(main, submit=True, part="both", readme_update=True)
