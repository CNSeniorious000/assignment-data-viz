from functools import wraps
from os import cpu_count, getenv
from typing import Callable, Iterable

from ..core.parse import File, Item
from .sum import sum_lists


def iter_maybe_with_progress[T](it: list[T], whether_to_show_progress: bool) -> Iterable[T]:
    if not whether_to_show_progress:
        return it

    from alive_progress import alive_it

    return alive_it(it)


JobArgs = tuple[int, int]


def as_worker[T](func: Callable[[Item], T]) -> Callable[[JobArgs], list[T]]:
    @wraps(func)
    def worker(args: JobArgs):
        n_jobs, index = args
        files = [file for i, file in enumerate(File.glob()) if i % n_jobs == index]
        return [func(item) for f in iter_maybe_with_progress(files, index == 0) for item in f.items]

    return worker


def dispatch_processes[T](func: Callable[[JobArgs], list[T]]):
    n_jobs = cpu_count() or 1
    if max_jobs := getenv("MAX_JOBS"):
        n_jobs = min(n_jobs, int(max_jobs))

    if n_jobs == 1:
        print(f"Running {func.__name__} in single-threaded mode")
        return func((1, 0))

    from concurrent.futures import ProcessPoolExecutor

    with ProcessPoolExecutor(max_workers=n_jobs) as executor:
        return sum_lists(executor.map(func, [(n_jobs, i) for i in range(n_jobs)]))
