from typing import Literal, TypedDict

Categories = Literal["harassment", "harassment/threatening", "hate", "hate/threatening", "self-harm", "self-harm/instructions", "self-harm/intent", "sexual", "sexual/minors", "violence", "violence/graphic"]


class Moderation(TypedDict):
    categories: dict[Categories, bool]
    """A list of the categories, and whether they are flagged or not."""

    category_scores: dict[Categories, float]
    """A list of the categories along with their scores as predicted by model."""

    flagged: bool
    """Whether any of the below categories are flagged."""


ModerationResultItem = tuple[int, Moderation]


all_categories: list[Categories] = ["harassment", "harassment/threatening", "hate", "hate/threatening", "self-harm", "self-harm/instructions", "self-harm/intent", "sexual", "sexual/minors", "violence", "violence/graphic"]
