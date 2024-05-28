from typing import Iterable

from promptools.openai import count_token

from .parse import File


def iter_maybe_with_progress[T](it: list[T], whether_to_show_progress: bool) -> Iterable[T]:
    if not whether_to_show_progress:
        return it

    from alive_progress import alive_it

    return alive_it(it)


def count_response_tokens(args: tuple[int, int]):
    n_job, index = args
    files = [file for i, file in enumerate(File.glob()) if i % n_job == index]
    return [count_token(item.response) for f in iter_maybe_with_progress(files, index == 0) for item in f.items]


def count_messages_tokens(args: tuple[int, int]):
    n_job, index = args
    files = [file for i, file in enumerate(File.glob()) if i % n_job == index]
    return [count_token(item.messages) for f in iter_maybe_with_progress(files, index == 0) for item in f.items]
