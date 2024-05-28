from asyncio import get_running_loop
from functools import cache
from typing import AsyncIterable, Callable, Iterable


@cache
def get_pool():
    from atexit import register
    from concurrent.futures import ThreadPoolExecutor

    pool = ThreadPoolExecutor()

    register(pool.shutdown)


__end_of_iteration = object()


async def iter_in_threadpool[T](it: Iterable[T]) -> AsyncIterable[T]:
    pool = get_pool()
    loop = get_running_loop()

    it = iter(it)

    while True:
        res = await loop.run_in_executor(pool, next, it, __end_of_iteration)
        if res is __end_of_iteration:
            return
        yield res  # type: ignore


async def call_in_threadpool[T, **P](fn: Callable[P, T], *args: P.args, **kwargs: P.kwargs):
    pool = get_pool()
    loop = get_running_loop()

    return await loop.run_in_executor(pool, lambda: fn(*args, **kwargs))
