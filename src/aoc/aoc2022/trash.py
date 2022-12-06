from enum import Enum
from typing import NamedTuple


def question_01_part_a():

    def part_a():
        container = []
        for x in txt.split("\n\n"):
            data = x.split()
            data = list(map(int, data))
            container.append(sum(data))
        return max(container)


def question_02():

    class Outcome(Enum):
        LOSE = "X"
        DRAW = "Y"
        WIN = "Z"

        def get_score(self) -> int:
            return {
                Outcome.LOSE: 0,
                Outcome.DRAW: 3,
                Outcome.WIN: 6
            }[self]

        def move(self, op: "Score") -> "Score":
            return {
                Outcome.DRAW: op,
                Outcome.WIN: op.counter_op(),
                Outcome.LOSE: op.counter_win()
            }[self]

    class Score(Enum):
        ROCK = "A"
        PAPER = "B"
        SCISSOR = "C"

        def get_score(self) -> int:
            return {
                Score.ROCK: 1,
                Score.PAPER: 2,
                Score.SCISSOR: 3
            }[self]

        def counter_op(self) -> "Score":
            return {
                Score.ROCK: Score.PAPER,
                Score.PAPER: Score.SCISSOR,
                Score.SCISSOR: Score.ROCK
            }[self]

        @staticmethod
        def parse(parser: str) -> "Score":
            return {
                "X": Score.ROCK,
                "Y": Score.PAPER,
                "Z": Score.SCISSOR
            }[parser]

        def counter_win(self) -> "Score":

            return {
                Score.ROCK: Score.SCISSOR,
                Score.SCISSOR: Score.PAPER,
                Score.PAPER: Score.ROCK
            }[self]

        def move(self, op_most: "Score") -> "Outcome":
            if self == op_most:
                return Outcome.DRAW
            condition = NamedTuple("Condition", [("self", Score), ("op", Score), ("outcome", Outcome)])
            conditions = [
                condition(Score.ROCK, Score.PAPER, Outcome.LOSE),
                condition(Score.ROCK, Score.SCISSOR, Outcome.WIN),
                condition(Score.PAPER, Score.ROCK, Outcome.WIN),
                condition(Score.PAPER, Score.SCISSOR, Outcome.LOSE),
                condition(Score.SCISSOR, Score.ROCK, Outcome.LOSE),
                condition(Score.SCISSOR, Score.PAPER, Outcome.WIN),
            ]

            for c in conditions:
                if self == c.self and op_most == c.op:
                    return c.outcome

            raise ValueError(f"Invalid condition {self} {op_most}")

    def part_a(txt: str) -> int:

        return sum(
            my_choice.get_score() + my_choice.move(op_choice).get_score() for op_choice, my_choice in ((
                Score(op_move),
                Score.parse(my_move)) for op_move, my_move in (line.split() for line in txt.splitlines())))

    def part_b(txt: str) -> int:

        return sum(
            my_move.move(op_move).get_score() + my_move.get_score() for op_move, my_move in ((
                Score(op_choice),
                Outcome(my_choice)) for op_choice, my_choice in (line.split() for line in txt.splitlines())))
