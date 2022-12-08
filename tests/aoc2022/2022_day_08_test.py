from src.aoc.aoc2022 import day_08 as d

TEST_INPUT = """
30373
25512
65332
33549
35390
""".strip()


def test_a() -> None:
    assert d.part_a(TEST_INPUT) == 21


def test_b() -> None:
    assert d.part_b(TEST_INPUT) == 8
