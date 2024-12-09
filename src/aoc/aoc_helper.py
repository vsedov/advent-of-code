import cProfile
import importlib
import os
import pstats
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from timeit import default_timer as timer
from typing import Any, Callable, Dict, List, Literal, Optional, Tuple, Union

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
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} PB"

@dataclass
class PyPerfResult:
    mean: float
    stdev: float
    median: Optional[float] = None
    min_time: Optional[float] = None
    max_time: Optional[float] = None
    warnings: List[str] = field(default_factory=list)
    calibration_data: Dict[str, Any] = field(default_factory=dict)
    benchmark_info: Dict[str, Any] = field(default_factory=dict)

    @property
    def coefficient_of_variation(self) -> float:
        return 0 if self.mean == 0 else (self.stdev / self.mean) * 100

    def is_stable(self, cv_threshold: float = 15.0) -> bool:
        return self.coefficient_of_variation < cv_threshold

@dataclass
class ComplexityResult:
    time_complexity: str
    r_squared: float
    fit_graph: Optional[Any] = None

@dataclass
class PerformanceMetrics:
    execution_time_us: float
    time_std_us: float
    memory_bytes: float
    memory_peak: float
    cpu_percent: float
    complexity: Optional[ComplexityResult] = None
    pyperf_stats: Optional[PyPerfResult] = None
    result: Any = None
    profile_stats: Optional[pstats.Stats] = None

class ComplexityAnalyzer:
    @staticmethod
    def create_data_generator(data: str):
        lines = data.split("\n") if isinstance(data, str) else data
        total_size = len(lines)
        def data_generator(n: int) -> str:
            subset_size = max(1, int(n))
            subset_size = min(subset_size, total_size)
            return "\n".join(lines[:subset_size]) if isinstance(data, str) else lines[:subset_size]
        return data_generator, total_size

    @staticmethod
    def analyze(func: Callable, data: str) -> ComplexityResult:
        try:
            data_generator, data_size = ComplexityAnalyzer.create_data_generator(data)
            min_n = max(2, data_size // 10)
            best_fit, measurements = big_o.big_o(
                func, data_generator=data_generator,
                min_n=min_n, max_n=data_size,
                n_repeats=3, n_timings=3
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
            return ComplexityResult(time_complexity="Unable to determine", r_squared=0.0)

class Aoc:
    _pyperf_runner = None

    def __init__(self, day: int = int(datetime.now().day), years: int = int(datetime.now().year),
                 benchmark_mode: str = "quick"):
        self.day = day
        self.year = years
        self.benchmark_mode = benchmark_mode
        self.data = get_data(day=self.day, year=self.year)
        self.test_module = importlib.import_module(f"tests.aoc{self.year}.{self.year}_day_{self.day:02d}_test")
        self.process = psutil.Process()

    @property
    def pyperf_runner(self):
        if Aoc._pyperf_runner is None:
            is_jit = pyperf.python_has_jit()

            if self.benchmark_mode == "quick":
                processes = 3
                warmups = 10
            elif self.benchmark_mode == "normal":
                processes = 6 if is_jit else 12
                warmups = 100
            else:  # accurate mode
                processes = 6 if is_jit else 20
                warmups = 1000

            Aoc._pyperf_runner = pyperf.Runner(
                processes=processes,
                warmups=warmups,
                values=3,
                min_time=0.1,
                show_name=True
            )
        return Aoc._pyperf_runner

    def run_pyperf_analysis(self, func: Callable, warmups: int = 1000, repeats: int = 1000) -> Optional[PyPerfResult]:
        try:
            print("\nStarting PyPerf analysis...")

            # Configure runner for this specific benchmark
            self.pyperf_runner.args = None  # Reset args before new benchmark
            self.pyperf_runner.args = self.pyperf_runner.parse_args([
                '--worker',
                '--values', str(repeats),
                '--warmups', str(warmups),
                '--loops', '1000',  # Let PyPerf calibrate
                '--rigorous',
                '--processes', '30',
            ])

            # Run benchmark
            benchmark = self.pyperf_runner.bench_func(
                func.__name__,
                lambda: func(self.data)
            )

            if benchmark is None:
                return PyPerfResult(
                    mean=0.0,
                    stdev=0.0,
                    warnings=["Benchmark run failed and returned None"]
                )

            # Extract values and compute statistics
            values = benchmark.get_values()
            if not values:
                return PyPerfResult(
                    mean=0.0,
                    stdev=0.0,
                    warnings=["No values recorded in benchmark"]
                )

            # Calculate statistics
            result = PyPerfResult(
                mean=benchmark.mean(),
                stdev=benchmark.stdev() if len(values) > 1 else 0.0,
                median=np.median(values),
                min_time=min(values),
                max_time=max(values),
                calibration_data={
                    'total_loops': len(values),
                    'inner_loops': 1,
                    'total_runtime': sum(values)
                },
                benchmark_info={
                    'name': func.__name__,
                    'samples': len(values),
                }
            )

            # Analyze results
            warnings = []
            cv = result.coefficient_of_variation
            if cv > 15.0:
                warnings.append(f"High variability (CV={cv:.1f}%)")

            if len(values) >= 4:  # Only check outliers if we have enough samples
                q1, q3 = np.percentile(values, [25, 75])
                iqr = q3 - q1
                outliers = [x for x in values if x < (q1 - 1.5 * iqr) or x > (q3 + 1.5 * iqr)]
                if outliers:
                    warnings.append(f"Found {len(outliers)} outliers")

            if result.calibration_data['total_runtime'] < 1.0:
                warnings.append("Short runtime")

            result.warnings = warnings
            return result

        except Exception as e:
            error_msg = f"PyPerf analysis failed: {str(e)}"
            print(f"\n[red]Error: {error_msg}[/red]")
            import traceback
            traceback.print_exc()
            return PyPerfResult(mean=0.0, stdev=0.0, warnings=[error_msg])

    def analyze_performance(self, func: Callable, runs: int = 100, with_profile: bool = False,
                          analyze_complexity: bool = True, warmups: int = 5000, repeats: int = 10000) -> PerformanceMetrics:
        times = []
        start_mem = self.process.memory_info().rss
        peak_mem = start_mem
        result = None
        profile_stats = None
        complexity_result = None
        pyperf_result = self.run_pyperf_analysis(func, warmups, repeats)

        if analyze_complexity:
            complexity_result = ComplexityAnalyzer.analyze(func, self.data)

        if with_profile:
            profiler = cProfile.Profile()
            profiler.enable()
            result = func(self.data)
            profiler.disable()
            profile_stats = pstats.Stats(profiler)

        for _ in track(range(50), description="Running performance analysis..."):
            if hasattr(func, "cache"):
                func.cache.clear()
            pre_mem = self.process.memory_info().rss
            start = timer()
            result = func(self.data)
            end = timer()
            post_mem = self.process.memory_info().rss
            peak_mem = max(peak_mem, post_mem)
            times.append((end - start) * 1e6)

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
            profile_stats=profile_stats
        )

    def print_metrics(self, metrics: PerformanceMetrics, part: str):
        def format_time(t: float) -> str:
            if t < 0.000001: return f"{t*1e9:.1f}ns"
            if t < 0.001: return f"{t*1e6:.1f}µs"
            if t < 1: return f"{t*1000:.1f}ms"
            return f"{t:.2f}s"

        table = Table(box=box.ROUNDED, title=f"Part {part.upper()} Analysis")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        table.add_row("Result", str(metrics.result))
        table.add_row(
            "Execution Time",
            f"{format_time(metrics.execution_time_us/1e6)} ± {format_time(metrics.time_std_us/1e6)}"
        )
        if metrics.memory_bytes > 0:
            table.add_row("Memory Usage", format_memory(metrics.memory_bytes))
        if metrics.memory_peak > 0:
            table.add_row("Peak Memory", format_memory(metrics.memory_peak))
        if metrics.cpu_percent > 0:
            table.add_row("CPU Usage", f"{metrics.cpu_percent:.1f}%")
        if metrics.complexity:
            table.add_row(
                "Time Complexity",
                f"{metrics.complexity.time_complexity} (R² = {metrics.complexity.r_squared:.3f})"
            )
        console.print(table)

        if metrics.profile_stats:
            console.print("\n[bold cyan]Profile Details:[/bold cyan]")
            console.print("[dim]Top 10 functions by cumulative time:[/dim]")
            metrics.profile_stats.sort_stats("cumulative").print_stats(10)

        if metrics.pyperf_stats:
            if metrics.pyperf_stats.warnings:
                console.print("\n[yellow]PyPerf Warnings:[/yellow]")
                for warning in metrics.pyperf_stats.warnings:
                    console.print(f"⚠️  {warning}")

            stats = metrics.pyperf_stats
            console.print(f"\n[cyan]PyPerf Statistics:[/cyan]")
            console.print(f"Mean: {stats.mean*1e6:.0f} µs")
            console.print(f"Std Dev: ±{stats.stdev*1e6:.0f} µs")
            if stats.median:
                console.print(f"Median: {stats.median*1e6:.0f} µs")
            if stats.calibration_data:
                console.print(f"Runtime: {stats.calibration_data['total_runtime']:.2f}s")

    def run_test(self, part: Literal["a", "b"]) -> bool:
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

    def submit(self, answer, part=None) -> None:
        submit(answer, part=part, day=self.day, year=self.year)

    def get_data(self) -> str:
        return self.data

    def run_all_tests(self) -> None:
        import pytest
        pytest.main([f"tests/aoc{self.year}/{self.year}_day_{self.day:02d}_test.py", "-v"])

    def get_problem_name(self) -> str:
        puzzle = Puzzle(year=self.year, day=self.day)
        return puzzle.title

    def update_readme(self) -> None:
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
                if not any("| Day | Problem | Part A | Part B |" in line for line in lines):
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

    def run(self, func=None, submit: bool = False, part: Union[None, str] = None,
            readme_update: bool = False, profile: bool = False, analyze_complexity: bool = False,
            warmups: int =10, repeats: int =10, runs: int =10) -> Dict[str, PerformanceMetrics]:
        console.rule(f"[bold blue]Advent of Code {self.year} - Day {self.day}")
        metrics = {}

        if func is not None:
            with console.status("[cyan]Running main function..."):
                func(self.get_data())

        modules = importlib.import_module(f"src.aoc.aoc{self.year}.day_{self.day:02d}")

        parts_to_run = []
        if part == "a" or part == "both":
            parts_to_run.append("a")
        if part == "b" or part == "both":
            parts_to_run.append("b")

        test_results = {}
        console.print("\n[cyan]Running Tests:")
        for part_name in parts_to_run:
            test_results[part_name] = self.run_test(part_name)

        for part_name in parts_to_run:
            console.rule(f"[yellow]Part {part_name.upper()}")
            part_func = getattr(modules, f"part_{part_name}")

            if profile:
                metrics[part_name] = self.analyze_performance(
                    part_func,
                    runs=runs,
                    warmups=warmups,
                    repeats=repeats,
                    analyze_complexity=analyze_complexity,
                    with_profile=True
                )
                self.print_metrics(metrics[part_name], part_name)

            if test_results[part_name] and submit:
                with console.status(f"[green]Submitting part {part_name}..."):
                    try:
                        result = metrics[part_name].result if profile else part_func(self.data)
                        self.submit(result, part=part_name)
                        console.print(f"[green]✓ Part {part_name} submitted successfully")
                    except Exception as e:
                        console.print(f"[red]✗ Submission failed: {str(e)}")
            elif submit and not test_results[part_name]:
                console.print(f"[red]Skipping submission for part {part_name} - tests failed")

        if readme_update:
            with console.status("[blue]Updating README..."):
                self.update_readme()
            console.print("[green]✓ README updated")

        return metrics

if __name__ == "__main__":
    aoc = Aoc(day=1, years=2023)
    metrics = aoc.run(
        part="both",
        profile=True,
        analyze_complexity=True,
        warmups=1,
        repeats=5,
        runs=100,
        submit=False,
        readme_update=True
    )
