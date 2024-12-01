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
        readme_path = os.path.join(PROJECT_ROOT, f"src/aoc/aoc{self.year}", "readme.md")

        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(readme_path), exist_ok=True)

        # Initialize table headers
        table_headers = [
            "# Advent of Code Solutions\n",
            "\n",
            "| Day | Problem | Solution | Part A | Part B |\n",
            "|-----|---------|----------|---------|---------|",
        ]

        # Generate default table content for all 25 days
        default_table = []
        for day in range(1, 26):
            default_table.append(
                f"| {day:02d} | [?](https://adventofcode.com/{self.year}/day/{day}) | [Solution](day_{day:02d}.py) | :x: | :x: |\n"
            )

        try:
            # Try to read existing content
            with open(readme_path, "r") as f:
                lines = f.readlines()

            # If file exists but doesn't have table, create new
            if not any("| Day | Problem |" in line for line in lines):
                lines = table_headers + ["\n"] + default_table

        except FileNotFoundError:
            # Create new file with default table
            lines = table_headers + ["\n"] + default_table

        # Update the specific day's entry
        removed_leading_zero = str(self.day).lstrip("0")
        day_found = False

        for i, line in enumerate(lines):
            if f"day/{removed_leading_zero})" in line:
                day_found = True
                # Get current status
                current_line = line

                # Update problem name
                if "[?]" in current_line:
                    current_line = current_line.replace(
                        f"[?](https://adventofcode.com/{self.year}/day/{removed_leading_zero})",
                        f"[{self.get_problem_name()}](https://adventofcode.com/{self.year}/day/{removed_leading_zero})",
                    )

                # Update completion status based on test results
                test_a_passed = self.run_test("a")
                test_b_passed = self.run_test("b")

                # Replace status markers
                parts = current_line.split("|")
                if test_a_passed:
                    parts[-2] = " :heavy_check_mark: "
                if test_b_passed:
                    parts[-1] = " :heavy_check_mark: |\n"

                lines[i] = "|".join(parts)
                break

        # If day wasn't found in existing table, add it
        if not day_found:
            new_line = (
                f"| {self.day:02d} "
                f"| [{self.get_problem_name()}](https://adventofcode.com/{self.year}/day/{removed_leading_zero}) "
                f"| [Solution](day_{self.day:02d}.py) "
                f"| {'✓' if self.run_test('a') else '❌'} "
                f"| {'✓' if self.run_test('b') else '❌'} |\n"
            )
            lines.append(new_line)

        # Write back to file
        with open(readme_path, "w") as f:
            f.writelines(lines)

    def run_all_tests(self) -> None:
        __import__("os").system("uv run pytest")

    def custom_solve(self) -> None:
        solve(year=self.year, day=self.day, data=self.get_data())

    def get_problem_name(self) -> str:
        puzzle = Puzzle(year=self.year, day=self.day)
        return puzzle.title
