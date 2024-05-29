from typing import Counter

from .core.count import count_messages_tokens, count_response_tokens
from .core.parse import File
from .utils.multiprocessing import dispatch_processes
from .utils.output import save_output


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

    save_output(
        "distributions",
        {
            "total": total_count,
            "conversation_length": Counter(conversation_lengths),
            "response_token": Counter(response_tokens),
            "messages_token": Counter(messages_tokens),
        },
    )
