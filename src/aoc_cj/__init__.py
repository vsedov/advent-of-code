import importlib
import inspect
import logging
import os
from pathlib import Path
from typing import Literal, Optional, Union

from aocd import submit

PROJECT_ROOT = Path(__file__).parent.parent.parent
LOGS_DIR = PROJECT_ROOT / "logs"
LOGS_DIR.mkdir(exist_ok=True)

Answer = Optional[Union[int, str]]


logging.basicConfig(
    filename=LOGS_DIR / "aoc_cj.log",
    level=logging.DEBUG,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
)


def solve(name: str, year: int, day: int, data: str) -> tuple[Answer, Answer]:
    ans_a: Answer = None
    ans_b: Answer = None

    try:
        module = importlib.import_module(f"{__name__}.aoc{year}.day_{day:02d}")

        def solve_part(part: Literal["a", "b"]) -> Answer:
            if f := getattr(module, f"part_{part}", None):
                assert inspect.isfunction(f)

                resp = f(data)
                print(resp)
                assert resp is None or isinstance(resp, (int, str))
                return resp
            return None

        ans_a = solve_part("a")
        ans_b = solve_part("b")

        test_module = importlib.import_module(f"tests.aoc{year}.{year}_day_{day:02d}_test")
        test_pass = (False, False)
        if f := getattr(test_module, "test_a", None):
            assert inspect.isfunction(f)
            try:
                f()
                test_pass = (True, test_pass[1])
            except AssertionError:
                test_pass = (False, test_pass[1])
        if f := getattr(test_module, "test_b", None):
            assert inspect.isfunction(f)
            try:
                f()
                test_pass = (test_pass[0], True)
            except AssertionError:
                test_pass = (test_pass[0], False)

        if all(test_pass):

            print("Test passed")
            submit(ans_a, part="a", day=day, year=year)
            submit(ans_b, part="b", day=day, year=year)
            writeer_path = os.path.join(PROJECT_ROOT, f"src/aoc_cj/aoc{year}", "readme.md")
            with open(writeer_path, "r") as f:
                lines = f.readlines()
                for i, line in enumerate(lines):
                    removed_leading_zero = str(day).lstrip("0")
                    if f"| [?](https://adventofcode.com/{year}/day/{removed_leading_zero})" in line:
                        lines[i] = line.replace(
                            f"| [?](https://adventofcode.com/{year}/day/{removed_leading_zero})",
                            f"| [{name}](https://adventofcode.com/{year}/day/{removed_leading_zero})",
                        )

                    if f"| {day:02d} " in line:
                        lines[i].replace(":x:", ":heavy_check_mark:")
                        break

            with open(writeer_path, "w") as f:
                f.writelines(lines)
                f.close()

    except ModuleNotFoundError as e:
        raise NotImplementedError() from e
    except Exception as e:
        logging.exception("error while solving year=%s day=%s", year, day)
        raise e
    finally:
        logging.info("result for year=%s day=%s: (parta: %s, partb: %s)", year, day, ans_a, ans_b)

    return ans_a, ans_b
