import pytest

from src.aoc.aoc2024 import day_02 as d

TEST_INPUT = """
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
""".strip()


def test_a() -> None:
    assert d.part_a(TEST_INPUT) == 2


def test_b() -> None:
    assert d.part_b(TEST_INPUT) == 4
