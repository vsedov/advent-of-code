from src.aoc.aoc2024 import YEAR, get_day
from src.aoc.aoc_helper import Aoc
from collections import defaultdict
import itertools

def parse(txt: str):
    antennas_by_freq = defaultdict(list)
    for y, line in enumerate(txt.splitlines()):
        for x, c in enumerate(line):
            if c != '.':
                antennas_by_freq[c].append(x + y * 1j)
    return antennas_by_freq, len(txt.splitlines()), len(txt.splitlines()[0])

def part_a(txt: str) -> int:
    antennas_by_freq, height, width = parse(txt)
    antinode_locations = set()

    for antennas in antennas_by_freq.values():
        if len(antennas) < 2:
            continue
        for a, b in itertools.combinations(antennas, 2):
            diff = a - b
            if diff:
                antinode_locations.add(a + diff)
                antinode_locations.add(b - diff)

    return sum(0 <= pos.real < width and 0 <= pos.imag < height
              for pos in antinode_locations)

def part_b(txt: str) -> int:
    antennas_by_freq, height, width = parse(txt)
    max_dim = max(height, width)
    antinode_locations = set()

    for antennas in antennas_by_freq.values():
        if len(antennas) < 2:
            continue
        antinode_locations.update(antennas)
        for a, b in itertools.combinations(antennas, 2):
            if diff := a - b:
                antinode_locations.update(a + i * diff for i in range(-max_dim, max_dim + 1))
                antinode_locations.update(b + i * diff for i in range(-max_dim, max_dim + 1))

    return sum(0 <= pos.real < width and 0 <= pos.imag < height
              for pos in antinode_locations)

def main(txt: str) -> None:
    print("part_a: ", part_a(txt))
    print("part_b: ", part_b(txt))

if __name__ == "__main__":
    aoc = Aoc(day=get_day(), years=YEAR)
    aoc.run(main, submit=False, part='both', readme_update=True, profile=True, analyze_complexity=True)
