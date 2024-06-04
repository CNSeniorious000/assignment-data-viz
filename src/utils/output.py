from functools import wraps
from typing import Callable

from msgspec.json import decode, encode

from ..utils.path import root

root /= "data/output"

if not root.exists():
    root.mkdir(parents=True)


def persist_to_json(filename: str):
    file = (root / filename).with_suffix(".json")

    def decorator[T](func: Callable[[], T]) -> Callable[[], T]:
        @wraps(func)
        def wrapper():
            if file.exists():
                return decode(file.read_bytes())
            res = func()
            file.write_bytes(encode(res))
            return res

        return wrapper

    return decorator
