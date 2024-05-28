from asyncio import Semaphore, ensure_future, gather
from pathlib import Path
from typing import Callable, Iterable

from aiofiles import open
from alive_progress import alive_bar
from msgspec.msgpack import encode
from openai import APIError, AsyncOpenAI

from ..types.moderations import Moderation, ModerationResultItem
from ..utils.sk_pool import get_api_key, key_count
from ..utils.sync import call_in_threadpool, iter_in_threadpool
from .parse import File

client = AsyncOpenAI()


root = Path("data/moderations")

if not root.exists():
    root.mkdir(parents=True)


BATCH_SIZE = 5  # <=32
CONCURRENCY = 3 * key_count


class ModerationPipeline:
    def __init__(self):
        self.semaphore = Semaphore(CONCURRENCY)

    async def save(self, file_id: str, items: Iterable[ModerationResultItem]):
        path = (root / file_id).with_suffix(".msgpack")

        async with open(path, "ab") as file:
            for line_index, moderation in items:
                await file.write(encode((line_index, moderation)))

    async def moderate(self, strings: list[str]) -> list[Moderation]:
        while True:
            try:
                res = await client.moderations.create(input=strings, extra_headers={"Authorization": f"Bearer {get_api_key()}"} if key_count > 1 else None)
                return res.model_dump(include={"results"})["results"]
            except APIError as e:
                print(e.type, e.message)

    async def process_file(self, file: File, callback: Callable | None = None):
        if (root / file.path.name).with_suffix(".msgpack").exists():
            if callback:
                callback(await call_in_threadpool(lambda: file.length))
            return

        async with self.semaphore:
            strings = []
            indices = []
            items = []

            async def flush():
                if not strings:
                    return

                results = await self.moderate(strings)
                items.extend(zip(indices, results))

            line_index = 0

            async for line_index, item in iter_in_threadpool(enumerate(file.items)):
                if not item.response:  # empty response
                    continue

                indices.append(line_index)
                strings.append(item.response[-2000:])

                if callback:
                    callback()

                if len(strings) == BATCH_SIZE:
                    await flush()
                    strings.clear()
                    indices.clear()

            await flush()

            await self.save(file.path.name, items)

    async def process_every_file(self):
        total = await call_in_threadpool(lambda: sum(i.length for i in File.glob()))
        with alive_bar(total, title="Moderating") as bar:
            await gather(*map(ensure_future, (self.process_file(i, bar) for i in File.glob())))
