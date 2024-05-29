from collections import Counter

from .core.parse import Item
from .utils.language import detect_language
from .utils.multiprocessing import as_worker, dispatch_processes
from .utils.output import persist_to_json


@as_worker
def detect_response_language(item: Item):
    return detect_language(item.response)


@persist_to_json("languages")
def detect_all():
    return Counter(dispatch_processes(detect_response_language))


def main():
    results = Counter(detect_all())

    total = sum(results.values())
    for lang, count in results.most_common(5):
        print(f"{lang}: {count / total:.2%}")
