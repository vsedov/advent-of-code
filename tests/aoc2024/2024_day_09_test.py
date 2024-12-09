
import pytest

from src.aoc.aoc2024 import day_09 as d

TEST_INPUT = """
2333133121414131402
""".strip()


def test_a() -> None:
    assert d.part_a(TEST_INPUT) == 1928


def test_b() -> None:
    assert d.part_b(TEST_INPUT) == 2858

