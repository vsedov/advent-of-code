from functools import reduce

from src.aoc.aoc2022 import YEAR, get_day
from src.aoc.aoc_helper import Aoc


def get_elf_list(txt: str) -> list:
    return list(range(int(txt.split('-')[0]), int(txt.split('-')[1]) + 1))


def get_intersection(list_1: list, list_2: list) -> int:
    return len(reduce(lambda x, y: x.intersection(y), [set(list_1), set(list_2)]))


def check_duplicates(list_1: list, list_2: list) -> int:
    return get_intersection(list_1, list_2) >= len(sorted([list_1, list_2], key=len, reverse=False)[0])


def check_duplicates_v2(*strings: list) -> bool:
    return get_intersection(*strings) > 0


def part_a(txt: str) -> int:

    return sum(
        check_duplicates(
            get_elf_list(l_split.split(",")[0]),
            get_elf_list(l_split.split(",")[1]),
        )
        for l_split in txt.splitlines()
    )


def part_b(txt: str) -> int:

    return sum(
        check_duplicates_v2(
            get_elf_list(l_split.split(",")[0]),
            get_elf_list(l_split.split(",")[1]),
        )
        for l_split in txt.splitlines()
    )


def main(txt: str) -> None:
    print("part_a: ", part_a(txt))
    print("part_b: ", part_b(txt))


if __name__ == "__main__":
    aoc = Aoc(day=get_day(), years=YEAR)
    aoc.run(main, submit=True, part="both", readme_update=False)
