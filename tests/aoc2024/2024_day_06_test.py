import pytest

from src.aoc.aoc2024 import day_06 as d

TEST_INPUT = """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
""".strip()


def test_a() -> None:
    assert d.part_a(TEST_INPUT) == 41


def test_b() -> None:
    assert d.part_b(TEST_INPUT) == 6
