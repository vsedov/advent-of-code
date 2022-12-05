# create_file(day=5, year=2022)
import argparse

from src.aoc_cj.template import create_file

help_text = """
Create a new file for the Advent of Code challenge.

--create or -c: Create a new file for the challenge.
    params:
        day : int
        year : int
Example:
python3 -m src --c 5 2022
"""

parser = argparse.ArgumentParser(description=help_text)
parser.add_argument("--create", "-c", nargs=2, type=int, help="Create a new file for the challenge.")
args = parser.parse_args()

if args.create:
    create_file(day=args.create[0], year=args.create[1])
