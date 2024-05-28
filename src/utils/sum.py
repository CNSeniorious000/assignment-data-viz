from functools import reduce
from operator import iadd
from typing import Iterable


def sum_lists[T](it: Iterable[list[T]]) -> list[T]:
    return reduce(iadd, it, [])
