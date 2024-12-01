import pytest

from src.aoc.aoc2023 import day_01 as d

TEST_INPUT = """
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
""".strip()


def test_a() -> None:
    assert d.part_a(TEST_INPUT) == 142


def test_b() -> None:
    assert d.part_b(TEST_INPUT) == 281
