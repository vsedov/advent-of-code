from typing import Dict

from src.aoc.aoc2022 import YEAR, get_day
from src.aoc.aoc_helper import Aoc


class Data:

    def __init__(self, txt: str):
        self.directions = {
            "L": -1,
            "R": +1,
            "U": +1j,
            "D": -1j,
        }
        self.txt = txt
        self.rope = [0 + 0j for _ in range(10)]
        self.create_set()

    def create_set(self) -> None:
        self.set_1 = {self.rope[1]}
        self.set_2 = {self.rope[-1]}

    def parse(self) -> list:
        for line in self.txt.splitlines():
            x, y = line.split()
            num_iterations = int(y)
            for _ in range(num_iterations):
                for i in range(len(self.rope)):
                    if i == 0:
                        self.rope[i] += self.directions[x]
                    else:
                        diff = self.rope[i - 1] - self.rope[i]
                        if abs(diff) >= 2:
                            real = diff.real / abs(diff.real) if diff.real != 0 else 0
                            imag = diff.imag / abs(diff.imag) if diff.imag != 0 else 0
                            direction = complex(real, imag)
                            self.rope[i] += direction

                self.set_1.add(self.rope[1])
                self.set_2.add(self.rope[-1])


def part_a(txt: str) -> int:
    data = Data(txt)
    data.parse()
    return len(data.set_1)


def part_b(txt: str) -> int:
    data = Data(txt)
    data.parse()
    return len(data.set_2)


def main(txt: str) -> None:
    print("part_a: ", part_a(txt))
    print("part_b: ", part_b(txt))


if __name__ == "__main__":
    aoc = Aoc(day=get_day(), years=YEAR)
    aoc.run(main, submit=True, part='both', readme_update=True)
