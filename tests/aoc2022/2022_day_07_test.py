import pytest

from src.aoc.aoc2022 import day_07 as d

TEST_INPUT = """
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
""".strip()


def test_a() -> None:
    assert d.part_a(TEST_INPUT) == 95437


def test_b() -> None:
    assert d.part_b(TEST_INPUT) == 24933642
