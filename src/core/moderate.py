from asyncio import Semaphore, ensure_future, gather
from pathlib import Path
from typing import Callable, Iterable

from aiofiles import open
from alive_progress import alive_bar
from msgspec.msgpack import encode
from openai import AsyncOpenAI

from ..types.moderations import Moderation, ModerationResultItem
from ..utils.sync import call_in_threadpool, iter_in_threadpool
from .parse import File

client = AsyncOpenAI()


root = Path("data/moderations")


BATCH_SIZE = 5  # <=32
CONCURRENCY = 3


class ModerationPipeline:
    def __init__(self) -> None:
        self.semaphore = Semaphore(CONCURRENCY)

    async def save(self, file_id: str, items: Iterable[ModerationResultItem]):
        path = (root / file_id).with_suffix(".msgpack")

        async with open(path, "ab") as file:
            for line_index, moderation in items:
                await file.write(encode((line_index, moderation)))

    async def moderate(self, strings: list[str]) -> list[Moderation]:
        res = await client.moderations.create(input=strings)
        return res.model_dump(include={"results"})["results"]

    async def process_file(self, file: File, callback: Callable | None = None):
        async with self.semaphore:
            strings = []
            items = []

            async def flush(current_line_index: int):
                results = await self.moderate(strings)
                items.extend(zip(range(current_line_index - len(strings), current_line_index), results))

            line_index = 0

            async for line_index, item in iter_in_threadpool(enumerate(file.items)):
                strings.append(item.response[-2000:])

                if callback:
                    callback()

                if len(strings) == BATCH_SIZE:
                    await flush(line_index)
                    strings.clear()

            await flush(line_index)

            await self.save(file.path.name, items)

    async def process_every_file(self):
        total = await call_in_threadpool(lambda: sum(i.length for i in File.glob()))
        with alive_bar(total, title="Moderating") as bar:
            await gather(*map(ensure_future, (self.process_file(i, bar) for i in File.glob())))
