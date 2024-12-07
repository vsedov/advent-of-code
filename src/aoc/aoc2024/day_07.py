from functools import partial
from itertools import product
from typing import Callable, Set, Tuple

import numpy as np
from numba import njit, prange
from numba.typed import List

from src.aoc.aoc2024 import YEAR, get_day
from src.aoc.aoc_helper import Aoc


@njit(cache=True)
def str_len(n: int) -> int:
    if n == 0:
        return 1
    length = 0
    while n > 0:
        length += 1
        n //= 10
    return length


@njit(cache=True)
def concat_nums(a: int, b: int) -> int:
    return a * (10 ** str_len(b)) + b


@njit(cache=True)
def evaluate(nums: np.ndarray, ops: np.ndarray, with_concat: bool = False) -> int:
    result = int(nums[0])
    for i in range(len(ops)):
        val = int(nums[i + 1])
        if ops[i] == 0:
            result += val
        elif ops[i] == 1:
            result *= val
        elif with_concat and ops[i] == 2:
            result = concat_nums(result, val)
    return result


@njit(cache=True, parallel=True)
def check_ops_batch(
    nums: np.ndarray, all_ops: np.ndarray, target: int, with_concat: bool
) -> np.ndarray:
    results = np.zeros(len(all_ops), dtype=np.bool_)
    for i in prange(len(all_ops)):
        results[i] = evaluate(nums, all_ops[i], with_concat) == target
    return results


def solve(txt: str, eval_func: Callable, n_ops: int = 2) -> int:
    def parse_line(line: str) -> Tuple[int, np.ndarray]:
        target, nums_str = line.split(": ")
        return int(target), np.array([int(x) for x in nums_str.split()], dtype=np.int64)

    total = 0
    ops_cache = {}

    for target, nums in map(parse_line, txt.splitlines()):
        n = len(nums) - 1

        if n not in ops_cache:
            ops = list(product(range(n_ops), repeat=n))
            ops_cache[n] = np.array(ops, dtype=np.int64)

        results = check_ops_batch(
            nums, ops_cache[n], target, eval_func.keywords["with_concat"]
        )
        if np.any(results):
            total += target

    return total


def part_a(txt: str) -> int:
    return solve(txt, partial(evaluate, with_concat=False), n_ops=2)


def part_b(txt: str) -> int:
    return solve(txt, partial(evaluate, with_concat=True), n_ops=3)


def main(txt: str) -> None:
    dummy_nums = np.array([1, 2], dtype=np.int64)
    dummy_ops = np.array([[0]], dtype=np.int64)
    check_ops_batch(dummy_nums, dummy_ops, 3, False)

    print("part_a: ", part_a(txt))
    print("part_b: ", part_b(txt))


if __name__ == "__main__":
    aoc = Aoc(day=get_day(), years=YEAR)
    aoc.run(main, submit=False, part="both", readme_update=True, profile=False)
