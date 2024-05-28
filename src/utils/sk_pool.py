from functools import partial
from itertools import cycle
from os import getenv

if api_keys := getenv("OPENAI_API_KEYS"):
    keys = api_keys.split(",")
    _cycle = cycle(keys)
    get_api_key = _cycle.__next__
    key_count = len(keys)
else:
    get_api_key = partial(getenv, "OPENAI_API_KEY")
    key_count = 1
