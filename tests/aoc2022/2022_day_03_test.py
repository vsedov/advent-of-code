import pytest

from src.aoc_cj.aoc2022 import day_03 as d

TEST_INPUT = """
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
""".strip()


def test_a():
    assert d.part_a(TEST_INPUT) == 157


def test_b():
    assert d.part_b(TEST_INPUT) == 0
