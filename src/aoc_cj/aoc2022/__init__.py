import inspect
import os

YEAR = 2022


def get_day() -> int:
    return int(os.path.basename(inspect.stack()[1].filename).split("_")[1].split(".")[0])
