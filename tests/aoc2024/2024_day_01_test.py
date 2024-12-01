from src.aoc.aoc2024 import day_01 as d

TEST_INPUT = """
3   4
4   3
2   5
1   3
3   9
3   3
""".strip()


def test_a() -> None:
    assert d.part_a(TEST_INPUT) == 11


def test_b() -> None:
    assert d.part_b(TEST_INPUT) == 31
