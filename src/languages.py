from collections import Counter

from .core.parse import Item
from .utils.language import detect_language
from .utils.multiprocessing import as_worker, dispatch_processes
from .utils.output import save_output


@as_worker
def detect_response_language(item: Item):
    return detect_language(item.response)


def main():
    results = dispatch_processes(detect_response_language)

    save_output("languages", Counter(results))
