from functools import cache


@cache
def get_detector():
    from lingua import LanguageDetectorBuilder

    return LanguageDetectorBuilder.from_all_languages().build()


def detect_language(text: str):
    language = get_detector().detect_language_of(text)
    if language is not None:
        return language.name
    return "-"
