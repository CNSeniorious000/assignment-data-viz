from typing import Literal, NotRequired, TypedDict

from promplate import Message


class Body(TypedDict):
    messages: list[Message]
    response_format: NotRequired[dict[Literal["type"], Literal["json_object", "text"]]]


class Metadata(TypedDict):
    headers: dict[str, str]
    server: str | None
    time: float


class Extras(Metadata):
    response: str


class InputItem(TypedDict):
    body: Body
    extras: Extras


class OutputItem(Metadata):
    messages: list[Message]
