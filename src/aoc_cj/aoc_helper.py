import importlib
import inspect
from datetime import datetime
from typing import Any, Literal, Union

from aocd import get_data, submit
from aocd.models import Puzzle

from src.aoc_cj import solve


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

    def run(self, func=None, submit: bool = False, part: Union[None, str] = None, custom_solve: bool = False) -> None:
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
            modules = importlib.import_module(f"src.aoc_cj.aoc{self.year}.day_{self.day:02d}")
            if part == "both":
                self.submit_part_a(getattr(modules, "part_a")(self.get_data()))
                self.submit_part_b(getattr(modules, "part_b")(self.get_data()))
            elif part == "a":
                self.submit_part_a(getattr(modules, "part_a")(self.get_data()))
            elif part == "b":
                self.submit_part_b(getattr(modules, "part_b")(self.get_data()))

            if custom_solve:
                self.custom_solve(self.get_problem_name())

    def run_test(self, part: Literal["a", "b"]) -> bool:
        if f := getattr(self.test_module, f"test_{part}", None):
            assert inspect.isfunction(f)
            try:
                f()
                return True
            except AssertionError:
                return False
        return False

    def run_all_tests(self) -> None:
        __import__("os").system("poetry run pytest")

    def custom_solve(self, name: str) -> None:
        solve(name=name, year=self.year, day=self.day, data=self.get_data())

    def get_problem_name(self) -> str:
        puzzle = Puzzle(year=self.year, day=self.day)
        soup = puzzle._soup()
        return soup.find("h2").text.replace("---", "").replace(f"Day {self.day}:", "").strip()
