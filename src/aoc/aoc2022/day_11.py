import math
from dataclasses import dataclass
from typing import List

from parse import parse

from src.aoc.aoc2022 import YEAR, get_day
from src.aoc.aoc_helper import Aoc


class Monkee:

    def __init__(self, monkee_num, starting_items, operation, test, throw_to_true, throw_to_false):
        self.number: int = monkee_num
        self.starting_items: list = starting_items
        self.operation = lambda old: eval(operation)
        self.test = test
        self.throw_to_true = int(throw_to_true)
        self.throw_to_false = int(throw_to_false)
        self.iter = 0

    def get_item(self):
        self.iter += 1
        return self.starting_items.pop(0)


def custom_string_parser(str: str) -> Monkee:
    result = parse(
        "Monkey {}:\n  Starting items: {}\n  Operation: new = {}\n  Test: divisible by {}\n    If true: throw to monkey {}\n    If false: throw to monkey {}",
        str)
    return Monkee(
        result[0], list(map(int, result[1].split(", "))), result[2], int(result[3]), int(result[4]), int(result[5]))


def parse_input(txt: str) -> List:

    return [custom_string_parser(monkey) for monkey in txt.split("\n\n")]


def monkeeee(txt, iteration_amount=20, mod=3) -> int:
    for _ in range(iteration_amount):
        for monkey in txt:
            while len(monkey.starting_items) > 0:
                worry: str = monkey.operation(monkey.get_item())
                worry = worry // mod if mod == 3 else worry % mod
                txt[monkey.throw_to_true].starting_items.append(worry) if worry % int(monkey.test) == 0 else txt[
                    monkey.throw_to_false].starting_items.append(worry)

    return math.prod(sorted([monkey.iter for monkey in txt], reverse=True)[:2])


def part_a(txt: str) -> int:
    txt: Monkee = parse_input(txt)
    return monkeeee(txt, 20, 3)


def part_b(txt: str) -> int:
    txt: List[Monkee] = parse_input(txt)
    mod = 1
    for m in txt:
        mod *= m.test

    return monkeeee(txt, 10000, mod)


def main(txt: str) -> None:
    print("part_a: ", part_a(txt))
    print("part_b: ", part_b(txt))


if __name__ == "__main__":
    aoc = Aoc(day=get_day(), years=YEAR)
    aoc.run(main, submit=True, part='both', readme_update=True)
