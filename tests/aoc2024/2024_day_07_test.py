import pytest

from src.aoc.aoc2024 import day_07 as d

TEST_INPUT = """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
""".strip()


def test_a() -> None:
    assert d.part_a(TEST_INPUT) == 3749


def test_b() -> None:
    assert d.part_b(TEST_INPUT) == 11387
