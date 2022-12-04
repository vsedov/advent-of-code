# Create templates based on the current day
import datetime
import inspect
import os

now = datetime.datetime.now()
day = now.day
year = now.year

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


def create_file(day=day, year=year) -> None:
    day = day
    year = year
    day_str = f"{day:02d}"
    year_str = f"{year}"
    project_path = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))))

    day_path = os.path.join(project_path, "src", "aoc_cj", f"aoc{year_str}")
    day_file = os.path.join(day_path, f"day_{day_str}.py")
    test_path = os.path.join(project_path, "tests", f"aoc{year_str}")
    test_file = os.path.join(test_path, f"{year}_day_{day_str}_test.py")

    check_path_file(day_path, day_file)
    check_path_file(test_path, test_file)

    create_template(day_file, CORE_FILE, day_str, year_str)
    create_template(test_file, TEST_TEMPLATE, day_str, year_str)


def create_template(file, template, day_str=day, year_str=year,) -> None:
    if os.stat(file).st_size == 0:
        with open(file, "w") as f:
            f.write(template.format(DAY=day_str, YEAR=year_str))


def check_path_file(path, file) -> None:
    if not os.path.exists(path):
        os.makedirs(path)

    if not os.path.exists(file):
        with open(file, "w") as f:
            f.write("")
    else:
        print(f"File {file} already exists")


create_file(day=5, year=2022)
