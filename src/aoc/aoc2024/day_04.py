from collections.abc import Iterator
from itertools import product

from src.aoc.aoc2024 import YEAR, get_day
from src.aoc.aoc_helper import Aoc


def ray(grid: list[str], x: int, y: int, dx: int, dy: int) -> str:
    return "".join(
        grid[y + dy * i][x + dx * i]
        for i in range(4)
        if 0 <= y + dy * i < len(grid) and 0 <= x + dx * i < len(grid[0])
    )


def part_a(txt: str) -> int:
    grid = txt.splitlines()
    return sum(
        ray(grid, x, y, dx, dy) == "XMAS"
        for (y, x), (dy, dx) in product(
            (
                (y, x)
                for y, row in enumerate(grid)
                for x, c in enumerate(row)
                if c == "X"
            ),
            [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)],
        )
    )


def part_b(txt: str) -> int:
    grid = txt.splitlines()
    return sum(
        all(
            grid[y + dy1][x + dx1] + grid[y + dy2][x + dx2] in ("MS", "SM")
            for (dy1, dx1), (dy2, dx2) in [((-1, -1), (1, 1)), ((-1, 1), (1, -1))]
        )
        for y, row in enumerate(grid[1:-1], 1)
        for x, c in enumerate(row[1:-1], 1)
        if c == "A"
    )


def main(txt: str) -> None:
    print("part_a: ", part_a(txt))
    print("part_b: ", part_b(txt))


if __name__ == "__main__":
    aoc = Aoc(day=get_day(), years=YEAR)
    aoc.run(main, submit=True, part="both", readme_update=True)

# def part_a(txt: str) -> int:
#     grid = txt.splitlines()
#     directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
#
#     count = 0
#     for y in range(len(grid)):
#         for x in range(len(grid[0])):
#             if grid[y][x] == "X":
#                 for dy, dx in directions:
#                     if ray(grid, x, y, dx, dy) == "XMAS":
#                         count += 1
#     return count
