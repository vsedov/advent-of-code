import importlib
import inspect
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Literal, Union

from aocd import get_data, submit
from aocd.models import Puzzle
from icecream import ic

from src.aoc import solve

PROJECT_ROOT = Path(__file__).parent.parent.parent


def warn(s):
    logging.warning(s)


def info(s):
    logging.info(s)


ic.configureOutput(outputFunction=info)


class Aoc:

    def __init__(self, day: int = int(datetime.now().day), years: int = int(datetime.now().year)):
        self.day = day
        self.year = years
        self.data = get_data(day=self.day, year=self.year)
        self.test_module = importlib.import_module(f"tests.aoc{self.year}.{self.year}_day_{self.day:02d}_test")

    def submit(self, answer, part=None) -> None:
        submit(answer, part=part, day=self.day, year=self.year)

    def get_data(self) -> str:
        return self.data

    def submit_part_a(self, answer) -> None:
        self.submit(answer, part="a")

    def submit_part_b(self, answer) -> None:
        self.submit(answer, part="b")

    def wrapper(self, func) -> Any:
        answer = func(self.get_data())
        self.submit(answer)
        return answer

    def run(self, func=None, submit: bool = False, part: Union[None, str] = None, readme_update: bool = False) -> None:
        """Run a function and submit the answer to the website.
        func : Main Function to run
            This need to be the outside function, although it can be None
        submit : Submit:  boolean value, if True part can not be None
            Boolean : True | False
        part : If Submit is active
            'a' | 'b' | 'both' or None
        custom_solve : If True, it will run the custom solve function
            Boolean : True | False
            This function will test the test cases: test_a and test_b test the current part_a and part_b functions
            and will submit the answer to the website : it will also update the README.md file
        """
        if func is not None:
            func(self.get_data())

        if submit:
            modules = importlib.import_module(f"src.aoc.aoc{self.year}.day_{self.day:02d}")
            tests = (self.run_test("a"), self.run_test("b"))
            options = {
                "a": (0,),
                "b": (1,),
                "both": (0, 1),
            }
            ic(f"Tests: {tests}")
            ic(f"Current part: {part}")

            for i in options.get(part, ()):
                current_part = "a" if i == 0 else "b"
                ic(f"Part {current_part} is not passing the test cases")
                if tests[i]:
                    self.submit(getattr(modules, f"part_{current_part}")(self.get_data()), part=current_part)
                else:
                    ic.configureOutput(outputFunction=warn)
                    ic(f"Part {current_part} is not passing the test cases")

            if readme_update:
                self.update_readme()

    def run_test(self, part: Literal["a", "b"]) -> bool:
        if f := getattr(self.test_module, f"test_{part}", None):
            assert inspect.isfunction(f)
            try:
                f()
                return True
            except AssertionError:
                return False
        return False

    def update_readme(self) -> None:

        writeer_path = os.path.join(PROJECT_ROOT, f"src/aoc/aoc{self.year}", "readme.md")
        with open(writeer_path, "r+") as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                removed_leading_zero = str(self.day).lstrip("0")
                if f"| [?](https://adventofcode.com/{self.year}/day/{removed_leading_zero})" in line:
                    print(f"Found line {i}")
                    lines[i] = line.replace(
                        f"| [?](https://adventofcode.com/{self.year}/day/{removed_leading_zero})",
                        f"| [{self.get_problem_name()}](https://adventofcode.com/{self.year}/day/{removed_leading_zero})",
                    ).replace(" :x: ", ":heavy_check_mark:")

                    break
            f.seek(0)
            f.writelines(lines)
            f.truncate()

    def run_all_tests(self) -> None:
        __import__("os").system("poetry run pytest")

    def custom_solve(self) -> None:
        solve(year=self.year, day=self.day, data=self.get_data())

    def get_problem_name(self) -> str:
        puzzle = Puzzle(year=self.year, day=self.day)
        soup = puzzle._soup()
        return soup.find("h2").text.replace("---", "").replace(f"Day {self.day}:", "").strip()
