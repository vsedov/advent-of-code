import pytest

from src.aoc.aoc2024 import day_05 as d

TEST_INPUT = """
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
""".strip()


def test_a() -> None:
    assert d.part_a(TEST_INPUT) == 143


def test_b() -> None:
    assert d.part_b(TEST_INPUT) == 123
