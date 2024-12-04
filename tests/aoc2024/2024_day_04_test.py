import pytest

from src.aoc.aoc2024 import day_04 as d

TEST_INPUT = """
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASXC
""".strip()


def test_a() -> None:
    assert d.part_a(TEST_INPUT) == 18


def test_b() -> None:
    assert d.part_b(TEST_INPUT) == 9
