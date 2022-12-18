import numpy as np

from src.aoc.aoc2022 import YEAR, get_day
from src.aoc.aoc_helper import Aoc


def parser_part_a(np_data: np.ndarray, bool_list: np.ndarray) -> int:

    for i in range(np_data.shape[0]):
        for j in range(np_data.shape[1]):
            cond = [np_data[0:i, j], np_data[i, 0:j], np_data[i + 1:, j], np_data[i, j + 1:]]

            if i in (0, np_data.shape[0] - 1) or j in (0, np_data.shape[1] -
                                                       1) or min(list(map(np.max, cond))) < np_data[i, j]:
                bool_list[i, j] = True

    return np.sum(bool_list)


def parser_part_b(np_data: np.ndarray, bool_list: np.ndarray) -> int:
    for i in range(1, np_data.shape[0] - 1):
        for j in range(1, np_data.shape[1] - 1):
            total = 1
            # More so for readability
            cond = {
                "up": np_data[i - 1::-1, j],
                "down": np_data[i + 1:, j],
                "right": np_data[i, j + 1:],
                "left": np_data[i, j - 1::-1],
            }
            for dir in cond.values():
                direction = dir >= np_data[i, j]
                index = np.where(direction == 1)[0]
                total *= index[0] + 1 if len(index) > 0 else len(direction)

            bool_list[i, j] = total

    return np.max(bool_list)


def part_a(txt: str) -> int:

    np_data = np.array([list(map(int, list(x))) for x in txt.splitlines()], dtype=int)
    bool_list = np.full(np_data.shape, False, dtype=bool)
    return int(parser_part_a(np_data, bool_list))


def part_b(txt: str) -> int:
    np_data = np.array([list(map(int, list(x))) for x in txt.splitlines()], dtype=int)
    bool_list = np.full(np_data.shape, 0, dtype=int)

    return int(parser_part_b(np_data, bool_list))


def main(txt: str) -> None:
    print("part_a: ", part_a(txt))
    print("part_b: ", part_b(txt))


if __name__ == "__main__":
    aoc = Aoc(day=get_day(), years=YEAR)
    aoc.run(main, submit=True, part='both', readme_update=True)
