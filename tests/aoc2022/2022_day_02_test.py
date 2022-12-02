import pytest

from src.aoc_cj.aoc2022 import day_02 as d

TEST_INPUT = """
A Y
B X
C Z
""".strip()


def test_a():
    assert d.part_a(TEST_INPUT) == 15


def test_b():
    assert d.part_b(TEST_INPUT) == 12


@pytest.mark.skip(reason="CLI Fails")
def test_all():
    from aocd import get_data

    data = get_data(day=2, year=2022)
    assert d.part_a(data) == 15337
    assert d.part_b(data) == 11696
