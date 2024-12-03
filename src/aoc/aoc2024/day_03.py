import math
import re
from itertools import compress, starmap
from operator import methodcaller, mul
from typing import Iterator, Match

from src.aoc.aoc2024 import YEAR, get_day
from src.aoc.aoc_helper import Aoc

MUL = re.compile(r"mul\((?P<x>\d+),(?P<y>\d+)\)")
INSTRUCTION = re.compile(r"mul\(\d+,\d+\)|do\(\)|don't\(\)")


def instruction_processor(matches: Iterator[Match]) -> Iterator[int]:
    instructions = map(methodcaller("group", 0), matches)
    enabled_states = []
    state = True

    for instr in instructions:
        if instr == "do()":
            state = True
        elif instr == "don't()":
            state = False
        else:
            enabled_states.append(state)
            if state and (nums := MUL.match(instr)):
                yield math.prod(map(int, nums.groups()))


def part_a(txt: str) -> int:
    return sum(math.prod(map(int, m)) for m in MUL.findall(txt))


def part_b(txt: str) -> int:
    return sum(instruction_processor(INSTRUCTION.finditer(txt)))


def main(txt: str) -> None:
    print("part_a: ", part_a(txt))
    print("part_b: ", part_b(txt))


if __name__ == "__main__":
    aoc = Aoc(day=get_day(), years=YEAR)
    aoc.run(main, submit=True, part="both", readme_update=True)
