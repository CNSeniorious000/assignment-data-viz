from collections import Counter

from .core.parse import File
from .utils.language import detect_language
from .utils.output import save_output


def main():
    from alive_progress import alive_it

    results = [detect_language(i.response) for file in alive_it(File.glob()) for i in file.items]

    save_output("languages", Counter(results))
