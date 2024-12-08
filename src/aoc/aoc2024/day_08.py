from src.aoc.aoc2024 import YEAR, get_day
from src.aoc.aoc_helper import Aoc
import numpy as np
from collections import defaultdict
import itertools

def parse(txt: str):
    lines = txt.splitlines()
    height, width = len(lines), len(lines[0])
    scan = {}
    antennas_by_freq = defaultdict(list)

    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c != '.':
                pos = x + y * 1j
                scan[pos] = c
                antennas_by_freq[c].append(pos)

    return scan, antennas_by_freq

def part_a(txt: str) -> int:
    scan, antennas_by_freq = parse(txt)
    antinode_locations = set()

    for freq, antennas in antennas_by_freq.items():
        for a, b in itertools.combinations(antennas, 2):
            diff = a - b
            if abs(diff) > 0:
                antinode_locations.add(a + diff)  # Forward antinode
                antinode_locations.add(b - diff)  # Backward antinode

    lines = txt.splitlines()
    height, width = len(lines), len(lines[0])
    valid_antinodes = sum(1 for pos in antinode_locations
                         if 0 <= pos.real < width and 0 <= pos.imag < height)

    return valid_antinodes

def part_b(txt: str) -> int:
    scan, antennas_by_freq = parse(txt)
    lines = txt.splitlines()
    height, width = len(lines), len(lines[0])
    max_dim = max(height, width)
    antinode_locations = set()

    for freq, antennas in antennas_by_freq.items():
        if len(antennas) >= 2:
            antinode_locations.update(antennas)

        for a, b in itertools.combinations(antennas, 2):
            diff = a - b
            if abs(diff) > 0:
                for i in range(-max_dim, max_dim + 1):
                    antinode_locations.add(a + i * diff)
                    antinode_locations.add(b + i * diff)

    valid_antinodes = sum(1 for pos in antinode_locations
                         if 0 <= pos.real < width and 0 <= pos.imag < height)

    return valid_antinodes

def main(txt: str) -> None:
    print("part_a: ", part_a(txt))
    print("part_b: ", part_b(txt))

if __name__ == "__main__":
    aoc = Aoc(day=get_day(), years=YEAR)
    aoc.run(main, submit=False, part='both', readme_update=True, profile=True, analyze_complexity=True)
