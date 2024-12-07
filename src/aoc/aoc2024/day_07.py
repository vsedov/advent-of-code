from typing import Tuple

import numpy as np
from numba import njit, prange
from numba.typed import Dict
from numba.typed import List as NumbaList

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
def dp_line(nums: np.ndarray, target: int, with_concat: bool) -> bool:
    prev_reachable = Dict.empty(key_type=np.int64, value_type=np.bool_)
    prev_reachable[nums[0]] = True
    for i in range(1, len(nums)):
        current_num = nums[i]
        next_reachable = Dict.empty(key_type=np.int64, value_type=np.bool_)
        for val in prev_reachable.keys():
            new_val = val + current_num
            if abs(new_val) < 10**12:
                next_reachable[new_val] = True
            new_val = val * current_num
            if abs(new_val) < 10**12:
                next_reachable[new_val] = True
            if with_concat:
                new_val = concat_nums(val, current_num)
                if abs(new_val) < 10**12:
                    next_reachable[new_val] = True
        prev_reachable = next_reachable
    return target in prev_reachable


@njit(cache=True, parallel=True, fastmath=True)
def dp_solve_all(
    targets: np.ndarray, all_nums: NumbaList[np.ndarray], with_concat: bool
) -> int:
    total = 0
    for i in prange(len(targets)):
        if dp_line(all_nums[i], targets[i], with_concat):
            total += targets[i]
    return total


def solve_with_dp(txt: str, with_concat: bool = False) -> int:
    lines = txt.strip().split("\n")
    targets_list = []
    nums_list = []
    for line in lines:
        target_str, nums_str = line.split(": ")
        target = int(target_str)
        nums = np.array([int(x) for x in nums_str.split()], dtype=np.int64)
        targets_list.append(target)
        nums_list.append(nums)

    targets_arr = np.array(targets_list, dtype=np.int64)
    typed_nums_list = NumbaList()
    for arr in nums_list:
        typed_nums_list.append(arr)

    return dp_solve_all(targets_arr, typed_nums_list, with_concat)


def part_a(txt: str) -> int:
    return solve_with_dp(txt, with_concat=False)


def part_b(txt: str) -> int:
    return solve_with_dp(txt, with_concat=True)


def main(txt: str) -> None:
    print("part_a: ", part_a(txt))
    print("part_b: ", part_b(txt))


if __name__ == "__main__":
    aoc = Aoc(day=get_day(), years=YEAR)
    aoc.run(main, submit=False, part="both", readme_update=True, profile=True)
