from typing import Tuple

import numpy as np
import numpy.typing as npt
from numba import njit

from src.aoc.aoc2024 import YEAR, get_day
from src.aoc.aoc_helper import Aoc


@njit
def parse_rules(rules_array: npt.NDArray) -> npt.NDArray:
    n = np.max(rules_array) + 1
    dep_matrix = np.zeros((n, n), dtype=np.int8)
    for rule in rules_array:
        dep_matrix[rule[1], rule[0]] = 1
    return dep_matrix


@njit
def check_order(deps: npt.NDArray, sequence: npt.NDArray) -> bool:
    # sourcery skip: use-any, use-next
    n = len(sequence)
    seq_deps = deps[sequence]
    for i in range(n - 1):
        if np.any(seq_deps[i, sequence[i + 1 :]]):
            return False
    return True


@njit
def find_valid_order(deps: npt.NDArray, numbers: npt.NDArray) -> npt.NDArray:
    n = len(numbers)
    result = np.empty(n, dtype=np.int64)
    used = np.zeros(n, dtype=np.bool_)
    in_degree = np.zeros(n, dtype=np.int64)
    for i in range(n):
        in_degree[i] = np.sum(deps[numbers, numbers[i]])

    # O(n) topological sort
    for pos in range(n):
        next_idx = np.where(~used & (in_degree == 0))[0][0]
        result[pos] = numbers[next_idx]
        used[next_idx] = True
        # amortisation
        for j in range(n):
            if not used[j] and deps[numbers[next_idx], numbers[j]]:
                in_degree[j] -= 1

    return result


def parse(txt: str) -> Tuple[npt.NDArray[np.int64], npt.NDArray[np.int64]]:
    rules_txt, sequences_txt = txt.split("\n\n")

    return np.array(
        [line.split("|") for line in rules_txt.splitlines()], dtype=np.int64
    ), np.array(
        [
            np.fromstring(line, sep=",", dtype=np.int64)
            for line in sequences_txt.splitlines()
        ],
        dtype=object,
    )


def part_a(txt: str) -> int:
    rules_array, sequences = parse(txt)
    deps = parse_rules(rules_array)

    return sum(seq[len(seq) // 2] for seq in sequences if check_order(deps, seq))


def part_b(txt: str) -> int:
    rules_array, sequences = parse(txt)
    deps = parse_rules(rules_array)

    total = 0
    for seq in sequences:
        if not check_order(deps, seq):
            fixed_order = find_valid_order(deps, seq)
            total += fixed_order[len(fixed_order) // 2]
    return total


def main(txt: str) -> None:
    print("part_a: ", part_a(txt))
    print("part_b: ", part_b(txt))


if __name__ == "__main__":
    aoc = Aoc(day=get_day(), years=YEAR)
    aoc.run(main, submit=True, part="both", readme_update=True)

# @njit
# def check_order(deps: npt.NDArray, sequence: npt.NDArray) -> bool:
#     n = len(sequence)
#     for i in range(n):
#         curr = sequence[i]
#         for j in range(i + 1, n):
#             if deps[curr, sequence[j]] == 1:
#                 return False
#     return True
# @njit
# def check_order(deps: npt.NDArray, sequence: npt.NDArray) -> bool:
#     seen = np.zeros_like(deps[0], dtype=np.bool_)
#     for num in sequence:
#         if np.any(deps[num] & seen):
#             return False
#         seen[num] = True
#     return True
