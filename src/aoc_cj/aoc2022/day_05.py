from collections import namedtuple
from typing import Tuple

from src.aoc_cj.aoc2022 import YEAR, get_day
from src.aoc_cj.aoc_helper import Aoc


def input_parser(txt: str):
    stack, moves = txt.split("\n\n")
    return namedtuple("input", "setup moves")(
        stack.splitlines(), [tuple(int(i) for i in line.split() if i.isdigit()) for line in moves.splitlines()])


def create_stack(initial_stack: Tuple[str, ...]) -> list[list[str]]:
    stack = [[] for _ in range(len(initial_stack[-1].split()))]
    for line in reversed(initial_stack[:-1]):
        for i, crate in enumerate(line[1::4]):
            if crate != " ":
                stack[i].append(crate)
    return stack


def part_a(txt: str) -> str:
    pre_stack, moves = input_parser(txt)
    stack = create_stack(pre_stack)

    for move_amount, current, goto in moves:
        for _ in range(move_amount):
            stack[goto - 1].append(stack[current - 1].pop())
    return "".join(stack[i][-1] for i in range(len(pre_stack[-1].split())))


def part_b(txt: str) -> str:

    pre_stack, moves = input_parser(txt)
    stack = create_stack(pre_stack)

    for move_amount, current, goto in moves:
        stack[goto - 1].extend(stack[current - 1][-move_amount:])
        del stack[current - 1][-move_amount:]

    return "".join(stack[i][-1] for i in range(len(pre_stack[-1].split())))


def main(txt: str) -> None:
    print("part_a: ", part_a(txt))
    print("part_b: ", part_b(txt))


if __name__ == "__main__":
    aoc = Aoc(day=get_day(), years=YEAR)
    aoc.run(main, submit=True, part='both', readme_update=True)
