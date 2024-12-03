import pytest

from src.aoc.aoc2024 import day_03 as d

TEST_INPUT = """
xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
""".strip()

TEST_INPUT2 = """
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
""".strip()


def test_a() -> None:
    assert d.part_a(TEST_INPUT) == 161


def test_b() -> None:
    assert d.part_b(TEST_INPUT2) == 48
