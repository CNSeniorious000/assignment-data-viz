from asyncio import run
from collections import Counter

from alive_progress import alive_it
from numpy import save

from .core.moderate import ModerationPipeline, all_saved_files, stream_msgpack_chunks
from .types.moderations import Categories, Moderation, all_categories
from .utils.output import persist_to_json


@persist_to_json("flags")
def load_all_results():
    count = [0, 0]
    flags: list[Categories] = []
    for file in alive_it(all_saved_files()):
        data: list[tuple[int, Moderation]] = list(stream_msgpack_chunks(file.read_bytes()))
        for _, moderation in data:
            count[moderation["flagged"]] += 1
            flags.extend(k for k, v in moderation["categories"].items() if v)

    print("Flagged:", count[1], "Unflagged:", count[0])

    total = sum(count)
    counter = Counter(flags)
    for key, value in counter.items():
        print(f"{key}: {value / total:.2%}")

    return {"count": count, "flags": counter}


def moderations_as_embeddings():
    from numpy import asarray

    from .utils.path import root

    target = root / "data" / "embeddings.npy"
    if target.exists():
        return

    embeddings = []

    for file in alive_it(all_saved_files()):
        data: list[tuple[int, Moderation]] = list(stream_msgpack_chunks(file.read_bytes()))
        for _, moderation in data:
            scores = moderation["category_scores"]
            embeddings.append(asarray(scores[i] for i in all_categories))

    save(target, asarray(embeddings))


def main():
    run(ModerationPipeline().process_every_file())
    load_all_results()
    moderations_as_embeddings()
