import pytest

from src.aoc.aoc2022 import day_09 as d

TEST_INPUT = """
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
""".strip()


def test_a() -> None:
    assert d.part_a(TEST_INPUT) == 13


def test_b() -> None:
    assert d.part_b(TEST_INPUT) == 1
