import cProfile
import importlib
import inspect
import logging
import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from timeit import default_timer as timer
from typing import Any, Callable, Dict, Literal, Optional, Tuple, Union

import big_o
import numpy as np
import psutil
from aocd import get_data, submit
from aocd.models import Puzzle
from icecream import ic
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.text import Text
from rich.traceback import install

from src.aoc import solve

PROJECT_ROOT = Path(__file__).parent.parent.parent

# Setup rich console and error handling
install()
console = Console()


@dataclass
class PerformanceMetrics:
    """Stores performance metrics for a solution."""

    execution_time_us: float  # Execution time in microseconds
    time_std_us: float  # Standard deviation of execution time
    memory_mb: float  # Memory usage in megabytes
    cpu_percent: float  # CPU usage percentage
    complexity: str  # Algorithmic complexity estimation
    result: Any  # Solution result


class Aoc:
    """Main class for Advent of Code solution handling and performance analysis."""

    def __init__(
        self, day: int = int(datetime.now().day), years: int = int(datetime.now().year)
    ):
        """Initialize with specific day and year, defaulting to current date."""
        self.day = day
        self.year = years
        self.data = get_data(day=self.day, year=self.year)
        self.test_module = importlib.import_module(
            f"tests.aoc{self.year}.{self.year}_day_{self.day:02d}_test"
        )
        self.process = psutil.Process()

    def analyze_performance(self, func: Callable, runs: int = 10) -> PerformanceMetrics:
        """Analyze performance metrics using actual AoC data."""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("[cyan]Running performance analysis...", total=3)

            # Time analysis with multiple runs for statistical significance
            times = []
            for _ in range(runs):
                start = timer()
                result = func(self.data)
                times.append((timer() - start) * 1e6)  # Convert to microseconds
            progress.advance(task)

            # Memory analysis using process resources
            start_mem = self.process.memory_info().rss
            func(self.data)
            end_mem = self.process.memory_info().rss
            memory_used = (end_mem - start_mem) / (1024 * 1024)  # Convert to MB
            progress.advance(task)

            # Complexity analysis using input scaling
            try:

                def data_generator(n):
                    if isinstance(self.data, str):
                        lines = self.data.split("\n")
                        scaled_lines = lines[: max(1, int(len(lines) * n / len(lines)))]
                        return "\n".join(scaled_lines)
                    return self.data[:n]

                # data_generator -- Function returning input data of 'length' N.
                #                   Input data for the argument `func` is created as
                #                   `data_generator(N)`. Common data generators are defined
                #                   in the submodule `big_o.datagen`
                #
                # min_n, max_n, n_measures -- The execution time of func is measured
                #                             at `n_measures` points between `min_n` and
                #                             `max_n` (included)
                #
                # n_repeats -- Number of times func is called to compute execution time
                #              (return the cumulative time of execution)
                #
                # n_timings -- Number of times the timing measurement is repeated.
                #              The minimum time for all the measurements is kept.
                #
                best_fit, _ = big_o.big_o(
                    func,
                    data_generator=data_generator,
                    min_n=len(self.data) // 10,
                    max_n=len(self.data),
                    n_repeats=5,
                    n_timings=5,
                )
                complexity = str(best_fit)
            except Exception as e:
                console.print(f"[yellow]Warning: Complexity analysis failed: {str(e)}")
                complexity = "Unable to determine"
            progress.advance(task)

            return PerformanceMetrics(
                execution_time_us=np.mean(times),
                time_std_us=np.std(times),
                memory_mb=memory_used,
                cpu_percent=self.process.cpu_percent(),
                complexity=complexity,
                result=result,
            )

    def print_metrics(self, metrics: PerformanceMetrics, part: str):
        """Display performance metrics in a formatted table."""

        def format_time(t: float) -> str:
            if t < 0.000001:
                return f"{t*1e9:.1f}ns"
            if t < 0.001:
                return f"{t*1e6:.1f}µs"
            if t < 1:
                return f"{t*1000:.1f}ms"
            return f"{t:.2f}s"

        table = Table(show_header=False, box=None)
        table.add_row("[bold cyan]Result:", f"[green]{metrics.result}")
        table.add_row(
            "[bold cyan]Time:",
            f"[green]{format_time(metrics.execution_time_us/1e6)} ± {format_time(metrics.time_std_us/1e6)}",
        )
        table.add_row("[bold cyan]Memory:", f"[green]{metrics.memory_mb:.2f}MB")
        table.add_row("[bold cyan]CPU Usage:", f"[green]{metrics.cpu_percent:.1f}%")
        table.add_row("[bold cyan]Complexity:", f"[green]{metrics.complexity}")

        panel = Panel(
            table, title=f"[bold blue]Part {part.upper()} Analysis", border_style="blue"
        )
        console.print(panel)

    def run_test(self, part: Literal["a", "b"]) -> bool:
        """Run a specific test for the given part."""
        test_func = getattr(self.test_module, f"test_{part}", None)
        if not test_func:
            console.print(f"[red]✗ No test found for part {part}")
            return False

        try:
            test_func()
            console.print(f"[green]✓ Part {part} test passed")
            return True
        except AssertionError as e:
            console.print(f"[red]✗ Part {part} test failed: {str(e)}")
            return False
        except Exception as e:
            console.print(f"[red]✗ Error running part {part} test: {str(e)}")
            return False

    def run(
        self,
        func=None,
        submit: bool = False,
        part: Union[None, str] = None,
        readme_update: bool = False,
        profile: bool = True,
        runs: int = 1000,
    ) -> Dict[str, PerformanceMetrics]:
        """Main execution method handling tests, profiling, and submissions."""
        console.rule(f"[bold blue]Advent of Code {self.year} - Day {self.day}")
        metrics = {}

        if func is not None:
            with console.status("[cyan]Running main function..."):
                func(self.get_data())

        modules = importlib.import_module(f"src.aoc.aoc{self.year}.day_{self.day:02d}")

        for part_name in ("a", "b"):
            if part not in (part_name, "both"):
                continue

            console.rule(f"[yellow]Part {part_name.upper()}")
            part_func = getattr(modules, f"part_{part_name}")
            test_passed = self.run_test(part_name)

            if profile:
                metrics[part_name] = self.analyze_performance(part_func, runs)
                self.print_metrics(metrics[part_name], part_name)

            if test_passed and submit:
                with console.status(f"[green]Submitting part {part_name}..."):
                    self.submit(metrics[part_name].result, part=part_name)
                console.print(f"[green]✓ Part {part_name} submitted")

        if readme_update:
            with console.status("[blue]Updating README..."):
                self.update_readme()
            console.print("[green]✓ README updated")

        return metrics

    def submit(self, answer, part=None) -> None:
        """Submit an answer to Advent of Code."""
        submit(answer, part=part, day=self.day, year=self.year)

    def get_data(self) -> str:
        """Get the input data for the current day."""
        return self.data

    def update_readme(self) -> None:
        """Update the README with current progress."""
        readme_dir = os.path.join(PROJECT_ROOT, f"src/aoc/aoc{self.year}")
        readme_path = os.path.join(readme_dir, "readme.md")
        os.makedirs(readme_dir, exist_ok=True)

        table_headers = [
            f"# Advent of Code {self.year}\n\n",
            "| Day | Problem | Part A | Part B | Complete |\n",
            "|-----|---------|---------|---------|----------|\n",
        ]

        def create_row(day: int) -> str:
            return f"| {day:02d} | [?](https://adventofcode.com/{self.year}/day/{day}) | :x: | :x: | :x: |\n"

        try:
            with open(readme_path, "r") as f:
                lines = f.readlines()
                if not any(
                    "| Day | Problem | Part A | Part B |" in line for line in lines
                ):
                    lines = table_headers + [create_row(i) for i in range(1, 26)]
        except FileNotFoundError:
            lines = table_headers + [create_row(i) for i in range(1, 26)]

        with open(readme_path, "w") as f:
            for i, line in enumerate(lines):
                day_str = str(self.day).lstrip("0")
                if f"| {self.day:02d} |" in line or f"/{day_str})" in line:
                    part_a_passed = self.run_test("a")
                    part_b_passed = self.run_test("b")
                    completed = part_a_passed and part_b_passed

                    new_line = (
                        f"| {self.day:02d} | "
                        f"[{self.get_problem_name()}](https://adventofcode.com/{self.year}/day/{day_str}) | "
                        f"{'✓' if part_a_passed else '✗'} | "
                        f"{'✓' if part_b_passed else '✗'} | "
                        f"{'✓' if completed else '✗'} |\n"
                    )
                    lines[i] = new_line
                    break
            f.writelines(lines)

    def get_problem_name(self) -> str:
        """Get the title of the current day's problem."""
        puzzle = Puzzle(year=self.year, day=self.day)
        return puzzle.title
