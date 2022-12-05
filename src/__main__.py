# create_file(day=5, year=2022)
import argparse

from src.utils.template import create_file

help_text = """
Create a new file for the Advent of Code challenge.
"""

parser = argparse.ArgumentParser(description=help_text)
parser.add_argument("--create", "-c", nargs=2, type=int, help="Create a new file for the challenge. Format: -c 2 2022")

args = parser.parse_args()

if args.create:
    create_file(day=args.create[0], year=args.create[1])
