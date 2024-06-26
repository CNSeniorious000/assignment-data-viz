"""parse data from .jsonl.lz4 binary files"""

from functools import cache, cached_property
from itertools import starmap
from pathlib import Path

from attrs import define
from msgspec.json import decode
from promplate.prompt.chat import assistant

from ..types.chatlog import InputItem, Metadata


@define
class Item:
    index: int
    raw: bytes

    @cached_property
    def input_item(self) -> InputItem:
        return decode(self.raw)

    @property
    def response(self):
        return self.input_item["extras"]["response"]

    @property
    def messages(self):
        input_item = self.input_item
        return input_item["body"]["messages"] + [assistant > input_item["extras"]["response"]]

    @property
    def length(self):
        return len(self.messages)

    @property
    def headers(self):
        return self.input_item["extras"]["headers"]

    @property
    def metadata(self) -> Metadata:
        extras = self.input_item["extras"]
        return {"headers": extras["headers"], "server": extras.get("server", ""), "time": extras["time"]}

    def __repr__(self):
        return repr(self.messages)


@define
class File:
    path: Path

    @classmethod
    def glob(cls):
        return list(map(cls, Path("chatlog-dataset/data").glob("*")))

    @property
    def raw(self) -> bytes:
        from blosc2 import decompress

        return decompress(self.path.read_bytes())

    @property
    @cache
    def length(self):
        return self.raw.count(b"\n")

    @property
    def items(self):
        return starmap(Item, enumerate(self.raw.strip().split(b"\n")))

    @property
    def example(self):
        return next(self.items)

    def __hash__(self):
        return hash(self.path)
