
import pytest

from src.aoc.aoc2024 import day_08 as d

TEST_INPUT = """
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
""".strip()

TEST_INPUT_2 = """
T....#....
...T......
.T....#...
.........#
..#.......
..........
...#......
..........
....#.....
..........
""" .strip()
def test_a() -> None:
    assert d.part_a(TEST_INPUT) == 14


def test_b() -> None:
    assert d.part_b(TEST_INPUT) == 34

