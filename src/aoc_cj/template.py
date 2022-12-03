# Create templates based on the current day
import datetime
import inspect
import os

CORE_FILE = '''
from src.aoc_cj.aoc{YEAR} import YEAR, get_day
from src.aoc_cj.aoc_helper import Aoc


def part_a(txt: str) -> int:

    return 0


def part_b(txt: str) -> int:

    return 0


def main(txt: str) -> None:
    print("part_a: ", part_a(txt))
    print("part_b: ", part_b(txt))


if __name__ == "__main__":
    aoc = Aoc(day=get_day(), years=YEAR)
    aoc.run(main, submit=False, part = 'a',  custom_solve=False )
'''

TEST_TEMPLATE = '''
import pytest

from src.aoc_cj.aoc{YEAR} import day_{DAY} as d

TEST_INPUT = """
""".strip()


def test_a() -> None:
    assert d.part_a(TEST_INPUT) == 0


def test_b() -> None:
    assert d.part_b(TEST_INPUT) == 0

'''


def create_file() -> None:
    now = datetime.datetime.now()
    day = now.day
    year = now.year
    day_str = f"{day:02d}"
    year_str = f"{year}"
    project_path = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))))

    day_path = os.path.join(project_path, "src", "aoc_cj", f"aoc{year_str}")
    print(f"Creating day {day_str} in {day_path}")
    if not os.path.exists(day_path):
        os.mkdir(day_path)
        print(f"Created {day_path}")

    day_file = os.path.join(day_path, f"day_{day_str}.py")
    if not os.path.exists(day_file):
        with open(day_file, "w") as f:
            f.write(CORE_FILE.format(YEAR=year_str))
        print(f"Created {day_file}")
    else:
        print(f"{day_file} already exists")

    test_path = os.path.join(project_path, "tests", f"aoc{year_str}")
    print(f"Creating test {day_str} in {test_path}")
    if not os.path.exists(test_path):
        os.mkdir(test_path)
        print(f"Created {test_path}")

    test_file = os.path.join(test_path, f"{year_str}_day_{day_str}_test.py")
    if not os.path.exists(test_file):
        with open(test_file, "w") as f:
            f.write(TEST_TEMPLATE.format(YEAR=year_str, DAY=day_str))
        print(f"Created {test_file}")
