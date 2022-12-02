from src.aoc_cj import solve
from src.aoc_cj.aoc2022 import YEAR, get_day

part_1_score = {"A": {"X": 4, "Y": 8, "Z": 3}, "B": {"X": 1, "Y": 5, "Z": 9}, "C": {"X": 7, "Y": 2, "Z": 6}}

part_2_score = {"A": {"X": 3, "Y": 4, "Z": 8}, "B": {"X": 1, "Y": 5, "Z": 9}, "C": {"X": 2, "Y": 6, "Z": 7}}


def part_a(txt: str) -> int:
    return sum(
        max(part_1_score[op_choice][my_choice] for my_choice in choices)
        for op_choice, choices in (line.split() for line in txt.splitlines())
    )


def part_b(txt: str) -> int:
    return sum(
        max(part_2_score[op_choice][my_choice] for my_choice in choices)
        for op_choice, choices in (line.split() for line in txt.splitlines())
    )


def main(txt: str) -> None:
    print(f"part_a: {part_a(txt)}")
    print(f"part_b: {part_b(txt)}")


if __name__ == "__main__":
    from aocd import get_data

    day = get_day()

    solve("Rock Paper Scissors", YEAR, day, get_data(day=day, year=YEAR))
