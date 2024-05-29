from typing import Counter

from promptools.openai import count_token

from .core.parse import File, Item
from .utils.multiprocessing import as_worker, dispatch_processes
from .utils.output import persist_to_json


@as_worker
def count_response_tokens(item: Item):
    return count_token(item.response)


@as_worker
def count_messages_tokens(item: Item):
    return count_token(item.messages)


@persist_to_json("distributions")
def main():
    from alive_progress import alive_it

    files = File.glob()

    total_count = sum(i.length for i in alive_it(files))
    print(f"{total_count = }")

    conversation_lengths = [i.length for i in alive_it(files)]
    print(f"total_messages = {sum(conversation_lengths)}")

    response_tokens = dispatch_processes(count_response_tokens)
    print(f"total_response_tokens = {sum(response_tokens)}")

    messages_tokens = dispatch_processes(count_messages_tokens)
    print(f"total_messages_tokens = {sum(messages_tokens)}")

    return {
        "total": total_count,
        "conversation_length": Counter(conversation_lengths),
        "response_token": Counter(response_tokens),
        "messages_token": Counter(messages_tokens),
    }
