import pytest

from src.aoc.aoc2022 import day_06 as d

TEST_INPUT = """
bvwbjplbgvbhsrlpgdmjqwftvncz
""".strip()


def test_a() -> None:
    assert d.part_a(TEST_INPUT) == 5


def test_b() -> None:
    assert d.part_b(TEST_INPUT) == 23


@pytest.mark.parametrize(
    "test_input,expected", [("bvwbjplbgvbhsrlpgdmjqwftvncz", 5), ("nppdvjthqldpwncqszvftbrmjlhg", 6),
                            ("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 10), ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 11),],
)
def test_a_plug(test_input: str, expected: int) -> None:
    assert d.part_a(test_input) == expected


@pytest.mark.parametrize(
    "test_input, expected", [("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 19), ("bvwbjplbgvbhsrlpgdmjqwftvncz", 23),
                             ("nppdvjthqldpwncqszvftbrmjlhg", 23), ("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 29),
                             ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 26),],
)
def test_b_plus(test_input: str, expected: int) -> None:
    assert d.part_b(test_input) == expected
