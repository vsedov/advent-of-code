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
