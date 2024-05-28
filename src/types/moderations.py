from typing import Literal, TypedDict

Categorie = Literal["harassment", "harassment/threatening", "hate", "hate/threatening", "self-harm", "self-harm/instructions", "self-harm/intent", "sexual", "sexual/minors", "violence", "violence/graphic"]


class Moderation(TypedDict):
    categories: dict[Categorie, bool]
    """A list of the categories, and whether they are flagged or not."""

    category_scores: dict[Categorie, float]
    """A list of the categories along with their scores as predicted by model."""

    flagged: bool
    """Whether any of the below categories are flagged."""


ModerationResultItem = tuple[int, Moderation]
