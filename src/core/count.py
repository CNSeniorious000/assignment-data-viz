from promptools.openai import count_token

from ..utils.multiprocessing import as_worker
from .parse import Item


@as_worker
def count_response_tokens(item: Item):
    return count_token(item.response)


@as_worker
def count_messages_tokens(item: Item):
    return count_token(item.messages)
