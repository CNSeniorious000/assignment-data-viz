from os import cpu_count
from typing import Callable, Counter

from .core.count import count_messages_tokens, count_response_tokens
from .core.parse import File
from .utils.output import save_output
from .utils.sum import sum_lists


def dispatch_processes[T](func: Callable[[tuple[int, int]], list[T]]):
    n_job = min(cpu_count() or 1, 8)
    if n_job == 1:
        print(f"Running {func.__name__} in single-threaded mode")
        return func((1, 0))

    from multiprocessing import Pool

    with Pool(n_job) as pool:
        return sum_lists(pool.map(func, ((n_job, i) for i in range(n_job))))


def main():
    from alive_progress import alive_it

    files = File.glob()

    total_count = sum(i.length for i in alive_it(files))
    print(f"{total_count = }")

    conversation_lengths = [i.length for i in alive_it(files)]
    print(f"total_messages = {sum(conversation_lengths)}")

    response_tokens = dispatch_processes(count_response_tokens)
    print(f"total_response_tokens = {sum(response_tokens)}")

    messages_tokens = dispatch_processes(count_messages_tokens)
    print(f"total_messages_tokens = {sum(messages_tokens)}")

    save_output(
        "distributions",
        {
            "total": total_count,
            "conversation_length": Counter(conversation_lengths),
            "response_token": Counter(response_tokens),
            "messages_token": Counter(messages_tokens),
        },
    )
