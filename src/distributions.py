from typing import Counter

from alive_progress import alive_it
from promptools.openai import count_token

from .core.parse import File
from .utils.output import save_output


def main():
    files = File.glob()

    total_count = sum(i.length for i in alive_it(files, title="Counting conversations"))

    print(f"{total_count = }")

    conversation_length_distribution = Counter(i.length for i in alive_it(files, title="Counting conversation lengths"))
    last_message_token_distribution = Counter(count_token(j.response) for i in alive_it(files, title="Counting last message tokens") for j in i.items)
    conversation_token_distribution = Counter(count_token(j.messages) for i in alive_it(files, title="Counting conversation tokens") for j in i.items)

    save_output(
        "distributions",
        {
            "total": total_count,
            "conversation_length": conversation_length_distribution,
            "last_message_token": last_message_token_distribution,
            "conversation_token": conversation_token_distribution,
        },
    )
