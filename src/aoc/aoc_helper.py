import cProfile
import importlib
import os
import pstats
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from timeit import default_timer as timer
from typing import Any, Callable, Dict, Literal, Optional, Tuple, Union

import big_o
import numpy as np
import psutil
import pyperf
from aocd import get_data, submit
from aocd.models import Puzzle
from rich import box
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.progress import track
from rich.table import Table

PROJECT_ROOT = Path(__file__).parent.parent.parent
console = Console()


def format_memory(bytes_value: float) -> str:
    """Convert bytes to human readable format with appropriate unit"""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} PB"


@dataclass
class PyPerfResult:
    """Results from PyPerf benchmarking"""

    mean: float
    stdev: float
    median: Optional[float] = None
    min_time: Optional[float] = None
    max_time: Optional[float] = None
    warnings: list[str] = None

    def __post_init__(self):
        if self.warnings is None:
            self.warnings = []


@dataclass
class ComplexityResult:
    """Results from complexity analysis"""

    time_complexity: str
    r_squared: float
    fit_graph: Optional[Any] = None


@dataclass
class PerformanceMetrics:
    """Performance metrics for a solution"""

    execution_time_us: float  # Execution time in microseconds
    time_std_us: float  # Standard deviation
    memory_bytes: float  # Memory usage in bytes
    memory_peak: float  # Peak memory usage in bytes
    cpu_percent: float  # CPU usage
    complexity: Optional[ComplexityResult] = None  # Complexity analysis results
    pyperf_stats: Optional[PyPerfResult] = None  # PyPerf statistics
    result: Any = None  # Solution result
    profile_stats: Optional[pstats.Stats] = None  # Optional profiling stats


class ComplexityAnalyzer:
    """Analyzes time complexity of functions using big_o library"""

    @staticmethod
    def create_data_generator(data: str):
        """Creates an appropriate data generator based on input type"""
        lines = data.split("\n") if isinstance(data, str) else data
        total_size = len(lines)

        def data_generator(n: int) -> str:
            subset_size = max(1, int(n))
            subset_size = min(subset_size, total_size)

            if isinstance(data, str):
                return "\n".join(lines[:subset_size])
            return lines[:subset_size]

        return data_generator, total_size

    @staticmethod
    def analyze(func: Callable, data: str) -> ComplexityResult:
        """Analyze time complexity using big_o library"""
        try:
            data_generator, data_size = ComplexityAnalyzer.create_data_generator(data)
            min_n = max(2, data_size // 10)

            best_fit, measurements = big_o.big_o(
                func,
                data_generator=data_generator,
                min_n=min_n,
                max_n=data_size,
                n_repeats=3,
                n_timings=3,
            )

            r_squared = 0.0
            if measurements:
                try:
                    ns, times = zip(*measurements)
                    if len(ns) > 1:
                        r_squared = np.corrcoef(ns, times)[0, 1] ** 2
                except:
                    r_squared = 0.0

            return ComplexityResult(time_complexity=str(best_fit), r_squared=r_squared)
        except Exception as e:
            console.print(f"[yellow]Warning: Complexity analysis failed: {str(e)}")
            return ComplexityResult(
                time_complexity="Unable to determine", r_squared=0.0
            )


class Aoc:
    def __init__(
        self, day: int = int(datetime.now().day), years: int = int(datetime.now().year)
    ):
        self.day = day
        self.year = years
        self.data = get_data(day=self.day, year=self.year)
        self.test_module = importlib.import_module(
            f"tests.aoc{self.year}.{self.year}_day_{self.day:02d}_test"
        )
        self.process = psutil.Process()
        # Initialize single pyperf runner instance
        self.pyperf_runner = pyperf.Runner(processes=1, program_args=["--quiet"])

    def run_pyperf_analysis(
        self, func: Callable, warmups: int = 5, repeats: int = 15
    ) -> Optional[PyPerfResult]:
        """Run detailed PyPerf timing analysis."""
        try:
            benchmark = self.pyperf_runner.bench_func(
                func.__name__, lambda: func(self.data), warmups=warmups, loops=repeats
            )

            # Extract all core statistics
            mean = benchmark.mean()
            stdev = benchmark.stdev()

            # Get additional statistics if available
            stats = benchmark.get_stats()
            warnings = []

            # Check for benchmark stability
            if stdev > mean * 0.15:  # If stdev is more than 15% of mean
                warnings.append(
                    f"WARNING: the benchmark result may be unstable\n"
                    f"* the standard deviation ({stdev*1e6:.0f} us) is {stdev/mean*100:.0f}% of the mean ({mean*1e3:.2f} ms)\n"
                    f"\nTry to rerun the benchmark with more runs, values and/or loops.\n"
                    f"Run 'python -m pyperf system tune' command to reduce the system jitter.\n"
                    f"Use pyperf stats, pyperf dump and pyperf hist to analyze results."
                )

            return PyPerfResult(mean=mean, stdev=stdev, warnings=warnings)
        except Exception as e:
            return None

    def analyze_performance(
        self,
        func: Callable,
        runs: int = 10,
        with_profile: bool = False,
        analyze_complexity: bool = True,
        warmups: int = 10,
        repeats: int = 10,
    ) -> PerformanceMetrics:
        """Run comprehensive performance analysis"""
        times = []
        start_mem = self.process.memory_info().rss
        peak_mem = start_mem
        result = None
        profile_stats = None
        complexity_result = None
        pyperf_result = None

        # Run PyPerf analysis first
        pyperf_result = self.run_pyperf_analysis(func, warmups, repeats)

        # Analyze complexity if requested
        if analyze_complexity:
            complexity_result = ComplexityAnalyzer.analyze(func, self.data)

        # Profiling run if requested
        if with_profile:
            profiler = cProfile.Profile()
            profiler.enable()
            result = func(self.data)
            profiler.disable()
            profile_stats = pstats.Stats(profiler)

        # Basic performance measurement runs
        for _ in track(range(runs), description="Running performance analysis..."):
            if hasattr(func, "cache"):
                func.cache.clear()

            pre_mem = self.process.memory_info().rss
            start = timer()
            result = func(self.data)
            end = timer()
            post_mem = self.process.memory_info().rss
            peak_mem = max(peak_mem, post_mem)

            times.append((end - start) * 1e6)  # Convert to microseconds

        end_mem = self.process.memory_info().rss
        memory_used = end_mem - start_mem
        peak_memory_used = peak_mem - start_mem

        return PerformanceMetrics(
            execution_time_us=np.mean(times),
            time_std_us=np.std(times),
            memory_bytes=memory_used,
            memory_peak=peak_memory_used,
            cpu_percent=self.process.cpu_percent(),
            complexity=complexity_result,
            pyperf_stats=pyperf_result,
            result=result,
            profile_stats=profile_stats,
        )

    def print_metrics(self, metrics: PerformanceMetrics, part: str):
        """Display performance metrics in a nicely formatted table"""

        def format_time(t: float) -> str:
            if t < 0.000001:
                return f"{t*1e9:.1f}ns"
            if t < 0.001:
                return f"{t*1e6:.1f}µs"
            if t < 1:
                return f"{t*1000:.1f}ms"
            return f"{t:.2f}s"

        # Create metrics table with rounded box style
        table = Table(box=box.ROUNDED, title=f"Part {part.upper()} Analysis")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")

        # Add result first
        table.add_row("Result", str(metrics.result))

        # Add timing metrics from basic measurement
        table.add_row(
            "Execution Time",
            f"{format_time(metrics.execution_time_us/1e6)} ± {format_time(metrics.time_std_us/1e6)}",
        )

        # Add memory metrics
        if metrics.memory_bytes > 0:
            table.add_row("Memory Usage", format_memory(metrics.memory_bytes))
        if metrics.memory_peak > 0:
            table.add_row("Peak Memory", format_memory(metrics.memory_peak))

        if metrics.cpu_percent > 0:
            table.add_row("CPU Usage", f"{metrics.cpu_percent:.1f}%")

        # Add complexity information if available
        if metrics.complexity:
            table.add_row(
                "Time Complexity",
                f"{metrics.complexity.time_complexity} (R² = {metrics.complexity.r_squared:.3f})",
            )

        console.print(table)

        # Print profile stats if available
        if metrics.profile_stats:
            console.print("\n[bold cyan]Profile Details:[/bold cyan]")
            console.print("[dim]Top 10 functions by cumulative time:[/dim]")
            metrics.profile_stats.sort_stats("cumulative").print_stats(10)

        # Print PyPerf results if available
        if metrics.pyperf_stats:
            # Print any warnings from PyPerf
            if metrics.pyperf_stats.warnings:
                for warning in metrics.pyperf_stats.warnings:
                    console.print(f"\n{warning}")

            # Print the PyPerf mean and standard deviation
            console.print(
                f"\npart_{part}: Mean +- std dev: "
                f"{metrics.pyperf_stats.mean*1e6:.0f} us +- "
                f"{metrics.pyperf_stats.stdev*1e6:.0f} us"
            )

    def run_test(self, part: Literal["a", "b"]) -> bool:
        """Run test for a specific part"""
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
            console.print(f"[red]✗ Error in part {part} test: {str(e)}")
            return False

    def run(
        self,
        func=None,
        submit: bool = False,
        part: Union[None, str] = None,
        readme_update: bool = False,
        profile: bool = False,
        analyze_complexity: bool = False,
        warmups: int = 10,
        repeats: int = 10,
        runs: int = 1000,
    ) -> Dict[str, PerformanceMetrics]:
        """Main execution method with enhanced performance analysis options."""
        console.rule(f"[bold blue]Advent of Code {self.year} - Day {self.day}")
        metrics = {}

        # Run custom function if provided
        if func is not None:
            with console.status("[cyan]Running main function..."):
                func(self.get_data())

        # Import solution module
        modules = importlib.import_module(f"src.aoc.aoc{self.year}.day_{self.day:02d}")

        # Determine which parts to run
        parts_to_run = []
        if part == "a" or part == "both":
            parts_to_run.append("a")
        if part == "b" or part == "both":
            parts_to_run.append("b")

        # Run tests first and collect results
        test_results = {}
        console.print("\n[cyan]Running Tests:")
        for part_name in parts_to_run:
            test_results[part_name] = self.run_test(part_name)

        # Process each part
        for part_name in parts_to_run:
            console.rule(f"[yellow]Part {part_name.upper()}")
            part_func = getattr(modules, f"part_{part_name}")

            # Run performance analysis if requested
            if profile:
                metrics[part_name] = self.analyze_performance(
                    part_func,
                    runs=runs,
                    warmups=warmups,
                    repeats=repeats,
                    analyze_complexity=analyze_complexity,
                    with_profile=True,
                )
                self.print_metrics(metrics[part_name], part_name)

            # Handle submission
            if test_results[part_name] and submit:
                with console.status(f"[green]Submitting part {part_name}..."):
                    try:
                        result = (
                            metrics[part_name].result
                            if profile
                            else part_func(self.data)
                        )
                        self.submit(result, part=part_name)
                        console.print(
                            f"[green]✓ Part {part_name} submitted successfully"
                        )
                    except Exception as e:
                        console.print(f"[red]✗ Submission failed: {str(e)}")
            elif submit and not test_results[part_name]:
                console.print(
                    f"[red]Skipping submission for part {part_name} - tests failed"
                )

        # Update README if requested
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

    def run_all_tests(self) -> None:
        """Run all tests using pytest."""
        import pytest

        pytest.main(
            [f"tests/aoc{self.year}/{self.year}_day_{self.day:02d}_test.py", "-v"]
        )

    def get_problem_name(self) -> str:
        """Get the title of the current day's problem."""
        puzzle = Puzzle(year=self.year, day=self.day)
        return puzzle.title

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


if __name__ == "__main__":
    # Example usage
    aoc = Aoc(day=1, years=2023)

    # Run with all analysis features
    metrics = aoc.run(
        part="both",
        profile=True,
        analyze_complexity=True,
        warmups=1,
        repeats=5,
        runs=100,
        submit=False,
        readme_update=True,
    )
