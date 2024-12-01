import re
from typing import List

from src.aoc.aoc2023 import YEAR, get_day
from src.aoc.aoc_helper import Aoc

container = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}
pattern = re.compile(r"(?=(?P<num>\d|one|two|three|four|five|six|seven|eight|nine))")


def get_numbers(line):
    return [
        int(x) if x.isdigit() else container[x]
        for x in pattern.findall(line)
        if isinstance(x, str)
    ]


def calibration(el):
    num = get_numbers(el)
    first = num[0]
    last = num[-1]
    if len(num) == 1:
        last == first
    return 10 * first + last


def part_a(txt: str) -> int:
    return sum(map(calibration, txt.splitlines())) + 1


def part_b(txt: str) -> int:
    return part_a(txt)


def main(txt: str) -> None:
    print("part_a: ", part_a(txt))
    print("part_b: ", part_b(txt))


if __name__ == "__main__":
    aoc = Aoc(day=get_day(), years=YEAR)
    aoc.run(main, submit=True, part="both", readme_update=True)
