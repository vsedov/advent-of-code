import importlib
import inspect
import logging
from pathlib import Path
from typing import Literal, Optional, Union

PROJECT_ROOT = Path(__file__).parent.parent.parent
LOGS_DIR = PROJECT_ROOT / "logs"
LOGS_DIR.mkdir(exist_ok=True)

Answer = Optional[Union[int, str]]

logging.basicConfig(
    filename=LOGS_DIR / "aoc_cj.log",
    level=logging.DEBUG,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
)


def solve(year: int, day: int, data: str) -> tuple[Answer, Answer]:
    ans_a: Answer = None
    ans_b: Answer = None

    try:

        def solve_part(part: Literal["a", "b"]) -> Answer:
            if f := getattr(module, f"part_{part}", None):
                assert inspect.isfunction(f)
                resp = f(data)
                assert resp is None or isinstance(resp, (int, str))
                return resp
            return None

        module = importlib.import_module(f"src.aoc_cj.aoc{year}.day_{day:02d}")

        ans_a = solve_part("a")
        ans_b = solve_part("b")

    except ModuleNotFoundError as e:
        raise NotImplementedError() from e
    except Exception as e:
        logging.exception("error while solving year=%s day=%s", year, day)
        raise e
    finally:
        logging.info("result for year=%s day=%s: (parta: %s, partb: %s)", year, day, ans_a, ans_b)

    return ans_a, ans_b
