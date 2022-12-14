import pytest

from src.aoc.aoc2022 import day_03 as d

TEST_INPUT = """
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
""".strip()


def test_a() -> None:
    assert d.part_a(TEST_INPUT) == 157


def test_b() -> None:
    assert d.part_b(TEST_INPUT) == 70
