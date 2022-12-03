import string
from collections import Counter
from typing import Tuple

from src.aoc_cj.aoc2022 import YEAR, get_day
from src.aoc_cj.aoc_helper import Aoc

def convert_char(chr)->int:
    uper_case = string.ascii_uppercase
    lower_case = string.ascii_lowercase

    return list(range(27, 53))[uper_case.index(chr)] if chr in uper_case else list(range(
        1, 27))[lower_case.index(chr)] if chr in lower_case else 0


def split_data(data) -> Tuple[str, str]:
    half = len(data) // 2
    return data[:half], data[half:]


def check_duplicates(*strings) -> int:
    for i in strings:
        locals()[f"s_{strings.index(i)}"] = Counter(i)
        locals()[f"s_{strings.index(i)}"] = set(locals()[f"s_{strings.index(i)}"].keys())

    if len(strings) == 2:
        return convert_char(locals()["s_0"].intersection(locals()["s_1"]).pop())
    return convert_char(locals()["s_0"].intersection(locals()["s_1"], locals()[f"s_2"]).pop())


def part_a(txt: str) -> int:

    return sum(check_duplicates(*split_data(i)) for i in txt.splitlines())


def part_b(txt: str) -> int:

    return sum(check_duplicates(*txt.splitlines()[i:i + 3]) for i in range(0, len(txt.splitlines()), 3))


def main(txt: str) -> None:
    print(f"part_a: {part_a(txt)}")
    print(f"part_b: {part_b(txt)}")


if __name__ == "__main__":
    aoc = Aoc(day=get_day(), years=YEAR)
    aoc.run(main, submit=True, part="both")
