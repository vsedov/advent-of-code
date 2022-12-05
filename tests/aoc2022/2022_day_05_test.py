from src.aoc_cj.aoc2022 import day_05 as d

TEST_INPUT = """
    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
""".rstrip()


def test_a() -> None:
    assert d.part_a(TEST_INPUT) == "CMZ"


def test_b() -> None:
    assert d.part_b(TEST_INPUT) == "MCD"
