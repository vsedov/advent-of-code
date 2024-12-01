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
    def __init__(
        self, day: int = int(datetime.now().day), years: int = int(datetime.now().year)
    ):
        self.day = day
        self.year = years
        self.data = get_data(day=self.day, year=self.year)
        self.test_module = importlib.import_module(
            f"tests.aoc{self.year}.{self.year}_day_{self.day:02d}_test"
        )

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

    def run(
        self,
        func=None,
        submit: bool = False,
        part: Union[None, str] = None,
        readme_update: bool = False,
    ) -> None:
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
            modules = importlib.import_module(
                f"src.aoc.aoc{self.year}.day_{self.day:02d}"
            )
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
                    self.submit(
                        getattr(modules, f"part_{current_part}")(self.get_data()),
                        part=current_part,
                    )
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
                print(f"Test {part} Passed")
                return True
            except AssertionError:
                print(f"Test {part} failed")
                return False
        print(f"Test {part} failed")
        return False

    def update_readme(self) -> None:
        readme_dir = os.path.join(PROJECT_ROOT, f"src/aoc/aoc{self.year}")
        writeer_path = os.path.join(readme_dir, "readme.md")

        os.makedirs(readme_dir, exist_ok=True)

        table_headers = [
            f"# Advent of Code {self.year}\n",
            "\n",
            "| Day | Problem | Part A | Part B | Complete |\n",
            "|-----|---------|---------|---------|----------|\n",
        ]

        def create_table_row(day: int) -> str:
            return (
                f"| {day:02d} | "
                f"[?](https://adventofcode.com/{self.year}/day/{day}) | "
                f":x: | :x: | :x: |\n"
            )

        try:
            with open(writeer_path, "r") as f:
                lines = f.readlines()
                # Check if table exists and has correct format
                if not any(
                    "| Day | Problem | Part A | Part B |" in line for line in lines
                ):
                    lines = table_headers + [create_table_row(i) for i in range(1, 26)]
        except FileNotFoundError:
            lines = table_headers + [create_table_row(i) for i in range(1, 26)]

        with open(writeer_path, "w") as f:
            for i, line in enumerate(lines):
                removed_leading_zero = str(self.day).lstrip("0")
                if f"| {self.day:02d} |" in line or f"/{removed_leading_zero})" in line:
                    # Get test results
                    part_a_passed = self.run_test("a")
                    part_b_passed = self.run_test("b")
                    completed = part_a_passed and part_b_passed

                    # Create status markers
                    part_a_status = ":heavy_check_mark:" if part_a_passed else ":x:"
                    part_b_status = ":heavy_check_mark:" if part_b_passed else ":x:"
                    complete_status = ":heavy_check_mark:" if completed else ":x:"

                    # Create new line
                    new_line = (
                        f"| {self.day:02d} | "
                        f"[{self.get_problem_name()}](https://adventofcode.com/{self.year}/day/{removed_leading_zero}) | "
                        f"{part_a_status} | {part_b_status} | {complete_status} |\n"
                    )
                    lines[i] = new_line
                    break

            f.writelines(lines)

    def run_all_tests(self) -> None:
        __import__("os").system("uv run pytest")

    def custom_solve(self) -> None:
        solve(year=self.year, day=self.day, data=self.get_data())

    def get_problem_name(self) -> str:
        puzzle = Puzzle(year=self.year, day=self.day)
        return puzzle.title
