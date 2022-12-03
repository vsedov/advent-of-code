from src.aoc_cj.aoc2022 import day_01 as d

TEST_INPUT = """
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
"""


def test_a() -> None:
    assert d.part_a(TEST_INPUT) == 24000


def test_b() -> None:
    assert d.part_b(TEST_INPUT) == 45000
