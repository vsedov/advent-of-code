import re

from src.aoc.aoc2022 import YEAR, get_day
from src.aoc.aoc_helper import Aoc


def parse(txt: str) -> dict:
    path = []
    sizes = {}

    for line in txt.splitlines():
        head, tail = line.split(" ", maxsplit=1)
        if head == "$":
            if tail == "cd ..":
                path.pop()
            elif tail.startswith("cd "):
                path.append(tail[3:])
            elif tail == "ls":
                continue
            else:
                raise ValueError(f"Unexpected command: {line}")
        elif head == "dir":
            continue
        else:
            sizes[tuple(path)] = sizes.get(tuple(path), 0) + int(head)
    return sizes


def sum_dir(dirs: dict, lim: int = 100000) -> int:
    return sum(size for _, size in dirs.items() if size <= lim)


def dir_sizes(sizes: dict) -> dict:
    dirs = {}
    for path, size in sizes.items():
        path = list(path)
        while path:
            dirs[tuple(path)] = dirs.get(tuple(path), 0) + size
            path.pop()
    return dirs


def find_smallest(dir: dict, total: int, required: int, data: str) -> int:
    freespace = total - dir[('/',)]
    return min(size for _, size in dir_sizes(parse(data)).items() if (size > required - freespace) and (size < total))


def part_a(txt: str) -> int:
    return sum_dir(dir_sizes(parse(txt)))


def part_b(txt: str) -> int:
    return find_smallest(dir_sizes(parse(txt)), 70000000, 30000000, txt)


def main(txt: str) -> None:
    print("part_a: ", part_a(txt))
    print("part_b: ", part_b(txt))


if __name__ == "__main__":
    aoc = Aoc(day=get_day(), years=YEAR)
    aoc.run(main, submit=True, part='both', readme_update=True)
